
from datetime import datetime, timezone

from app.features.products.service import ProductService
from app.infra.cache.redis_service import RedisService
from app.features.products.constants import PRODUCT_CACHE_KEY_TAG
from app.shared.enrichers.product_enricher import ProductEnricher
from app.features.products.mappers.dto_mapper import ProductMapper
from app.features.products.product_dto import ProductDetailDTO

from app.features.pricing.services.catalog_pricing import (
    CatalogPricingService,
)
from app.features.pricing.dtos.catalog_pricing_dto import (
    CatalogPricingContext,
    CatalogPricingItemDTO,
)

from app.features.customer.customer_types import CustomerType
from app.features.orders.types.sale import SaleChannel


class GetProductByIdUseCase:

    def __init__(
        self,
        product_service: ProductService,
        cache_service: RedisService,
        product_enricher: ProductEnricher,
        catalog_pricing_service: CatalogPricingService,
    ):
        self._product_service = product_service
        self._cache_service = cache_service
        self._product_enricher = product_enricher
        self._catalog_pricing_service = catalog_pricing_service

    async def execute(
        self,
        product_id: int,
        customer_id: int | None = None,
        customer_type: CustomerType | None = None,
    ) -> ProductDetailDTO:

        cached_product = (
            await self._cache_service.get_or_set_with_lock_v2(
                tag=PRODUCT_CACHE_KEY_TAG,
                callback=self._get_product,
                kwargs={
                    "product_id": product_id,
                },
                key_args={
                    "product_id": product_id,
                },
                serializer=lambda product: product.to_dict(),
                deserializer=ProductDetailDTO.from_dict,
            )
        )

        product = ProductDetailDTO.from_dict(
            cached_product.to_dict()
        )

        pricing_context = CatalogPricingContext(
            items=[
                CatalogPricingItemDTO(
                    product_id=product.id,
                    category=product.category,
                    brand=product.brand,
                    unit_price=product.base_price,
                )
            ],
            sale_channel=SaleChannel.ECOMMERCE,
            customer_id=customer_id,
            customer_type=customer_type,
            now=datetime.now(timezone.utc),
        )

        pricing_results = (
            await self._catalog_pricing_service.calculate(
                context=pricing_context,
            )
        )

        if pricing_results:
            pricing = pricing_results[0]

            product.discount_price = pricing.discount_amount
            product.final_price = pricing.final_price

            product.applied_promotions = (
                pricing.applied_promotions
                if pricing.has_discount
                else []
            )

        return product

    async def _get_product(
        self,
        product_id: int,
    ) -> ProductDetailDTO:

        product = await (
            self._product_service.get_product_entity_by_id(
                product_id
            )
        )

        await self._product_enricher.attach_variant_images(
            [product]
        )

        return ProductMapper.to_product_detail_dto(
            product
        )
