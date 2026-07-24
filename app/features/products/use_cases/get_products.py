from app.features.products.service import ProductService
from app.infra.cache.redis_service import RedisService
from app.features.products.constants import PRODUCT_CACHE_KEY_TAG
from app.shared.enrichers.product_enricher import ProductEnricher
from app.features.products.mappers.dto_mapper import ProductMapper
from app.shared.pagination.pagination_service import PaginationService

from app.features.products.product_dto import FilterProductCommand, CatalogProductDTO


class GetProductsUseCase:

    def __init__(
        self,
        product_service: ProductService,
        cache_service: RedisService,
        pagination_service: PaginationService,
        product_enricher: ProductEnricher
    ):
        self._product_service = product_service
        self._cache_service = cache_service
        self._product_enricher = product_enricher
        self._pagination_service: PaginationService = pagination_service

    async def execute(
        self,
        command: FilterProductCommand,
        page: int = 1,
        limit: int = 20,
    ):

        return await self._cache_service.get_or_set_with_lock_v2(
            tag=PRODUCT_CACHE_KEY_TAG,
            callback=self._get_products,
            kwargs={
                "command": command,
                "page": page,
                "limit": limit
            },
            key_args={
                "filters": command.to_dict,
                "page": page,
                "limit": limit
            },
            serializer=lambda catalog: catalog.to_dict(),
            deserializer=CatalogProductDTO.from_dict
        )
    
    async def _get_products(
        self,
        command: FilterProductCommand,
        page: int,
        limit: int,
    ) -> CatalogProductDTO:
        
        total_items = await self._product_service.count_products(command)

        offset = self._pagination_service.get_offset(page, limit)

        total_pages = self._pagination_service.get_total_pages(total_items, limit)

        current_page = self._pagination_service.get_current_page(offset, limit)
        
        products = await self._product_service.get_products(
            command,
            offset,
            limit,
        )

        await self._product_enricher.attach_variant_images(
            products
        )

        return CatalogProductDTO.create(
            items=ProductMapper.to_grid_products(products),
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )