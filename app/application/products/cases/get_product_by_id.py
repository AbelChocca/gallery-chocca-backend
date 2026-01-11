from app.domain.product.entities.product import Product
from app.domain.cache.protocole import CacheProtocol
from app.domain.product.dto.product_dto import ReadProductDTO
from app.core.log.protocole import LoggerProtocol
from app.core.settings.pydantic_settings import Settings
from app.application.products.helper_mapper import ProductEntityToDTOMapper, ProductEntityToDictMapper, ProductDictToReadDTOMapper
from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository

from typing import Dict, Any

class GetProductByIDCase:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            image_repo: PostgresImageRepository,
            cache_service: CacheProtocol,
            settings_repo: Settings,
            logger: LoggerProtocol
            ):
        self.product_repo = product_repo
        self.image_repo = image_repo
        self.cache_service = cache_service
        self.logger = logger
        self.settings = settings_repo

    def _dict_to_dto(self, data: Dict[str, Any]) -> ReadProductDTO:
        return ProductDictToReadDTOMapper.to_read_dto(data)
    
    async def _get_and_sync_products_and_images(self, product_id: int) -> Product:
        product = await self.product_repo.get_by_id(product_id)
        images = await self.image_repo.get_images(
            owner_type="product_variant",
            owners_id=product.get_variants_id()
        )
        product.sync_images_to_variants(images)
        return product

    async def execute(self, product_id: int) -> ReadProductDTO:
        product_key: str = Product.get_filter_key(id=product_id)
        data: Dict[str, Any] = await self.cache_service.cache_get(product_key)

        if data:
            self.logger.info(f"Product with id:{product_id} was successfully get.")
            return self._dict_to_dto(data)
        
        if (await self.cache_service.cache_set_lock(key=product_key, seconds=self.settings.REDIS_LOCK_TTL)):
            product = await self._get_and_sync_products_and_images(product_id)

            value_to_encode = ProductEntityToDictMapper.to_read_dict(product)

            await self.cache_service.cache_set(key=product_key, data=value_to_encode, seconds=self.settings.REDIS_MEDIUM_TTL)

            self.logger.info(f"Product {product.nombre} was set to the cache service succesfully")
            return ProductEntityToDTOMapper.to_read_dto(product)   
        
        data = await self.cache_service.cache_retry_get(
            retries=self.settings.REDIS_MAX_RETRIES,
            seconds_delay=self.settings.REDIS_SECONDS_DELAY,
            key=product_key
        )
        if data:
            self.logger.info(f"Product with id:{product_id} was successfully get.")
            return self._dict_to_dto(data)

        product = await self._get_and_sync_products_and_images(product_id)
        self.logger.warning(f"⚠️ Product with id: {product_id} was getting from database after retry get from cache.")
        return ProductEntityToDTOMapper.to_read_dto(product)

