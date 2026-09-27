from datetime import datetime, timezone

from app.features.products.service import ProductService
from app.features.products.constants import PRODUCT_CACHE_KEY_TAG
from app.features.products.mappers.dto_mapper import ProductMapper
from app.features.products.product_dto import (
    FilterProductCommand,
    CatalogProductDTO,
    GridProductDTO,
)

from app.features.pricing.services.catalog_pricing import (
    CatalogPricingService,
)
from app.features.pricing.dtos.catalog_pricing_dto import (
    CatalogPricingContext,
    CatalogPricingItemDTO,
    CatalogPricingItemResultDTO,
)

from app.features.sales.types.customer import CustomerType
from app.features.sales.types.sale import SaleChannel

from app.infra.cache.redis_service import RedisService

from app.shared.enrichers.product_enricher import ProductEnricher
from app.shared.pagination.pagination_service import PaginationService


class GetProductsUseCase:

    def __init__(
        self,
        product_service: ProductService,
        cache_service: RedisService,
        pagination_service: PaginationService,
        product_enricher: ProductEnricher,
        catalog_pricing_service: CatalogPricingService,
    ):
        self._product_service = product_service
        self._cache_service = cache_service
        self._product_enricher = product_enricher
        self._pagination_service = pagination_service
        self._catalog_pricing_service = catalog_pricing_service

    async def execute(
        self,
        command: FilterProductCommand,
        customer_id: int | None = None,
        customer_type: CustomerType | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> CatalogProductDTO:

        catalog = await self._cache_service.get_or_set_with_lock_v2(
            tag=PRODUCT_CACHE_KEY_TAG,
            callback=self._get_products,
            kwargs={
                "command": command,
                "page": page,
                "limit": limit,
            },
            key_args={
                "filters": command.to_dict,
                "page": page,
                "limit": limit,
            },
            serializer=lambda catalog: catalog.to_dict(),
            deserializer=CatalogProductDTO.from_dict,
        )

        pricing_context = self._build_catalog_pricing_context(
            products=catalog.items,
            customer_id=customer_id,
            customer_type=customer_type,
        )

        pricing_results = (
            await self._catalog_pricing_service.calculate(
                context=pricing_context,
            )
        )

        self._apply_catalog_pricing(
            products=catalog.items,
            pricing_results=pricing_results,
        )

        return catalog

    async def _get_products(
        self,
        command: FilterProductCommand,
        page: int,
        limit: int,
    ) -> CatalogProductDTO:

        total_items = await self._product_service.count_products(
            command
        )

        offset = self._pagination_service.get_offset(
            page,
            limit,
        )

        total_pages = self._pagination_service.get_total_pages(
            total_items,
            limit,
        )

        current_page = self._pagination_service.get_current_page(
            offset,
            limit,
        )

        products = await self._product_service.get_products(
            command,
            offset,
            limit,
        )

        await self._product_enricher.attach_variant_images(
            products
        )

        grid_products = ProductMapper.to_grid_products(
            products
        )

        return CatalogProductDTO.create(
            items=grid_products,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )

    def _build_catalog_pricing_context(
        self,
        *,
        products: list[GridProductDTO],
        customer_id: int | None,
        customer_type: CustomerType | None,
    ) -> CatalogPricingContext:

        return CatalogPricingContext(
            items=[
                CatalogPricingItemDTO(
                    product_id=product.id,
                    category=product.category,
                    brand=product.brand,
                    unit_price=product.original_price,
                )
                for product in products
            ],
            sale_channel=SaleChannel.ECOMMERCE,
            customer_id=customer_id,
            customer_type=customer_type,
            now=datetime.now(timezone.utc),
        )

    def _apply_catalog_pricing(
        self,
        *,
        products: list[GridProductDTO],
        pricing_results: list[
            CatalogPricingItemResultDTO
        ],
    ) -> None:

        pricing_by_product = {
            result.product_id: result
            for result in pricing_results
        }

        for product in products:
            pricing = pricing_by_product.get(
                product.id
            )

            if pricing is None:
                continue

            product.original_price = (
                pricing.original_price
            )

            product.final_price = (
                pricing.final_price
            )

            product.discount_amount = (
                pricing.discount_amount
            )