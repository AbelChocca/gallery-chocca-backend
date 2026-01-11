from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.domain.product.entities.product import Product
from app.domain.cache.protocole import CacheProtocol
from app.core.log.protocole import LoggerProtocol
from app.core.settings.pydantic_settings import Settings
from app.domain.product.dto.product_dto import GetProductsResponseDTO
from app.application.products.commands import FilterProductCommand
from app.application.products.helper_mapper import ProductCommandToDTOMapper, ProductEntityToDTOMapper, ProductDictToReadDTOMapper, ProductEntityToDictMapper

from typing import Dict, Any, List


class GetProductsCase:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            image_repo: PostgresImageRepository,
            cache_service: CacheProtocol,
            settings: Settings,
            logger: LoggerProtocol
            ):
        self.product_repo: PostgresProductRepository = product_repo
        self.image_repo: PostgresImageRepository = image_repo
        self.cache_service: CacheProtocol = cache_service
        self.settings: Settings = settings
        self.logger: LoggerProtocol = logger

    def _dict_to_responde_dto(self, data: Dict[str, Any]) -> GetProductsResponseDTO:
        return GetProductsResponseDTO(
            total=data["total"],
            products=[
                ProductDictToReadDTOMapper.to_read_dto(
                    product_dict
                )
                for product_dict in data["products"]
            ]
        )
    async def _get_products_and_images_and_sync(
            self, 
            command: FilterProductCommand,
            offset: int,
            limit: int
        ) -> List[Product]:
        products = await self.product_repo.get_all(
            filter_dto=ProductCommandToDTOMapper.to_filter_dto(command),
            offset=offset,
            limit=limit
        )
        variant_ids: List[int] = []
        for product in products:
            variant_ids.extend(product.get_variants_id())

        images = await self.image_repo.get_images(
            owner_type="product_variant",
            owners_id=variant_ids
        )
        
        for product in products:
            product.sync_images_to_variants(images)

        return products

    async def _count_products(self, command: FilterProductCommand) -> int:
        res = await self.product_repo.count_filtered_products(
            filter_dto=ProductCommandToDTOMapper.to_filter_dto(command)
        )
        self.logger.info(f"Got it! total count products with filters: {res}")
        return res

    async def execute(
        self,
        command: FilterProductCommand,
        offset: int,
        limit: int,
    ) -> GetProductsResponseDTO:
        products_key: str = Product.get_filter_key(brand=command.marca, name=command.name, category=command.categoria, model=command.modelo, promotion=command.promocion, color=command.color)
        data = await self.cache_service.cache_get(key=products_key)
        if data:
            self.logger.info("Products with filter was successfully get.")
            return self._dict_to_responde_dto(data)

        if (await self.cache_service.cache_set_lock(key=products_key, seconds=self.settings.REDIS_LOCK_TTL)):
            count_products: int = await self._count_products(command)
            products = await self._get_products_and_images_and_sync(
                command=command,
                offset=offset,
                limit=limit
            )
            object_value = ProductEntityToDictMapper.products_to_response_dict(total_count=count_products, products=products)
            await self.cache_service.cache_set(key=products_key, data=object_value, seconds=self.settings.REDIS_MEDIUM_TTL)
            return self._dict_to_responde_dto(object_value)
        
        data = await self.cache_service.cache_retry_get(retries=self.settings.REDIS_MAX_RETRIES, key=products_key, seconds_delay=self.settings.REDIS_SECONDS_DELAY)
        if data:
            self.logger.info("Products with filter was successfully get from cache after few retries.")
            return self._dict_to_responde_dto(data)

        products_response = await self._get_products_and_images_and_sync(
            command=command,
            offset=offset,
            limit=limit
        )
        return GetProductsResponseDTO(
            total=self._count_products(command=command),
            products=[
                ProductEntityToDTOMapper.to_read_dto(product)
                for product in products_response
            ]
        )