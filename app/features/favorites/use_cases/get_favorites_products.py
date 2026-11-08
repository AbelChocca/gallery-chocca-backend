
from datetime import datetime, timezone

from app.features.favorites.service import FavoriteService
from app.features.favorites.dto import FavoritesFilterDto

from app.features.products.mappers.dto_mapper import ProductMapper
from app.features.products.product_dto import (
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

from app.features.customer.customer_types import CustomerType
from app.features.orders.types.sale import SaleChannel

from app.shared.pagination.pagination_service import PaginationService
from app.shared.enrichers.product_enricher import ProductEnricher


class GetFavoriteProductsUseCase:
    def __init__(
        self,
        favorite_service: FavoriteService,
        pagination_service: PaginationService,
        product_enricher: ProductEnricher,
        catalog_pricing_service: CatalogPricingService,
    ):
        self._favorite_service = favorite_service
        self._pagination_service = pagination_service
        self._product_enricher = product_enricher
        self._catalog_pricing_service = catalog_pricing_service

    async def execute(
        self,
        filter: FavoritesFilterDto,
        page: int = 1,
        limit: int = 20,
        session_id: str | None = None,
        user_id: int | None = None,
        customer_id: int | None = None,
        customer_type: CustomerType | None = None,
    ) -> CatalogProductDTO:
        offset = self._pagination_service.get_offset(
            page,
            limit,
        )

        if user_id is not None:
            products = (
                await self._favorite_service.get_favorites_by_user_id(
                    filter,
                    offset,
                    limit,
                    user_id,
                )
            )

            total = await self._favorite_service.count_favorites(
                user_id=user_id,
            )
        else:
            products = (
                await self._favorite_service.get_favorites_by_session_id(
                    filter,
                    offset,
                    limit,
                    session_id,
                )
            )

            total = await self._favorite_service.count_favorites(
                session_id=session_id,
            )

        await self._product_enricher.attach_variant_images(
            products
        )

        # Igual que el catálogo general.
        grid_products = ProductMapper.to_grid_products(
            products
        )

        pricing_context = self._build_catalog_pricing_context(
            products=grid_products,
            customer_id=customer_id,
            customer_type=customer_type,
        )

        pricing_results = (
            await self._catalog_pricing_service.calculate(
                context=pricing_context,
            )
            if grid_products
            else []
        )

        self._apply_catalog_pricing(
            products=grid_products,
            pricing_results=pricing_results,
        )

        return CatalogProductDTO.create(
            items=grid_products,
            total_items=total,
            current_page=self._pagination_service.get_current_page(
                offset,
                limit,
            ),
            total_pages=self._pagination_service.get_total_pages(
                total,
                limit,
            ),
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
        pricing_results: list[CatalogPricingItemResultDTO],
    ) -> None:
        pricing_by_product = {
            result.product_id: result
            for result in pricing_results
        }

        for product in products:
            pricing = pricing_by_product.get(product.id)

            if pricing is None:
                continue

            product.original_price = pricing.original_price
            product.final_price = pricing.final_price
            product.discount_amount = pricing.discount_amount
