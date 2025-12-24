from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.domain.entities.product import Product
from app.modules.cache.cache_repository import CacheRepository
from app.modules.product.domain.dto.product_dto import ReadProductDTO
from app.core.log.logger_repository import LoggerRepository
from app.core.settings.pydantic_settings import Settings
from app.application.products.helper_mapper import ProductEntityToDTOMapper, ProductEntityToDictMapper, ProductDictToReadDTOMapper

from typing import Dict, Any

class GetProductByIDCase:
    def __init__(
            self,
            repo: ProductRepository,
            cache_repo: CacheRepository,
            settings_repo: Settings,
            logger: LoggerRepository
            ):
        self.repo = repo
        self.cache_repo = cache_repo
        self.logger = logger
        self.settings = settings_repo

    def _dict_to_dto(self, data: Dict[str, Any]) -> ReadProductDTO:
        return ProductDictToReadDTOMapper.to_read_dto(data)

    async def execute(self, product_id: int) -> ReadProductDTO:
        product_key: str = Product.get_filter_key(id=product_id)
        data: Dict[str, Any] = await self.cache_repo.cache_get(product_key)

        if data:
            self.logger.info(f"Product with id:{product_id} was successfully get.")
            return self._dict_to_dto(data)
        
        if (await self.cache_repo.cache_set_lock(key=product_key, seconds=self.settings.REDIS_LOCK_TTL)):
            product = await self.repo.get_by_id(product_id)
            value_to_encode = ProductEntityToDictMapper.to_read_dict(product)

            await self.cache_repo.cache_set(key=product_key, data=value_to_encode, seconds=self.settings.REDIS_MEDIUM_TTL)

            self.logger.info(f"Product {product.nombre} was set to the cache service succesfully")
            return ProductEntityToDTOMapper.to_read_dto(product)   
        
        data = await self.cache_repo.cache_retry_get(
            retries=self.settings.REDIS_MAX_RETRIES,
            seconds_delay=self.settings.REDIS_SECONDS_DELAY,
            key=product_key
        )
        if data:
            self.logger.info(f"Product with id:{product_id} was successfully get.")
            return self._dict_to_dto(data)

        product = await self.repo.get_by_id(product_id)
        self.logger.warning(f"⚠️ Product with id: {product_id} was getting from database after retry get from cache.")
        return ProductEntityToDTOMapper.to_read_dto(product)

