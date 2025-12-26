from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.domain.entities.product import Product
from app.modules.cache.cache_repository import CacheRepository
from app.core.log.logger_repository import LoggerRepository
from app.core.settings.pydantic_settings import Settings
from app.modules.product.domain.dto.product_dto import GetProductsResponseDTO
from app.application.products.commands import FilterProductCommand
from app.application.products.helper_mapper import ProductCommandToDTOMapper, ProductEntityToDTOMapper, ProductDictToReadDTOMapper, ProductEntityToDictMapper

from typing import Dict, Any


class GetProductsCase:
    def __init__(
            self,
            repo: ProductRepository,
            cache_repo: CacheRepository,
            settings: Settings,
            logger: LoggerRepository
            ):
        self.repo: ProductRepository = repo
        self.cache_repo: CacheRepository = cache_repo
        self.settings: Settings = settings
        self.logger: LoggerRepository = logger

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

    async def _count_products(self, command: FilterProductCommand) -> int:
        res = await self.repo.count_filtered_products(
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
        products_key: str = Product.get_filter_key(name=command.name, category=command.categoria, model=command.modelo, promotion=command.promocion, color=command.color)
        data = await self.cache_repo.cache_get(key=products_key)
        if data:
            self.logger.info("Products with filter was successfully get.")
            return self._dict_to_responde_dto(data)

        if (await self.cache_repo.cache_set_lock(key=products_key, seconds=self.settings.REDIS_LOCK_TTL)):
            count_products: int = await self._count_products(command)
            products = await self.repo.get_all(
                offset=offset,
                limit=limit,
                filter_dto=ProductCommandToDTOMapper.to_filter_dto(command)
            )
            object_value = ProductEntityToDictMapper.products_to_response_dict(total_count=count_products, products=products)
            await self.cache_repo.cache_set(key=products_key, data=object_value, seconds=self.settings.REDIS_MEDIUM_TTL)
            return self._dict_to_responde_dto(object_value)
        
        data = await self.cache_repo.cache_retry_get(retries=self.settings.REDIS_MAX_RETRIES, key=products_key, seconds_delay=self.settings.REDIS_SECONDS_DELAY)
        if data:
            self.logger.info("Products with filter was successfully get from cache after few retries.")
            return self._dict_to_responde_dto(data)

        products_response = await self.repo.get_all(
                offset=offset,
                limit=limit,
                filter_dto=ProductCommandToDTOMapper.to_filter_dto(command)
            )
        return GetProductsResponseDTO(
            total=self._count_products(command=command),
            products=[
                ProductEntityToDTOMapper.to_read_dto(product)
                for product in products_response
            ]
        )