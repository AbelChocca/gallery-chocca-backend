from app.features.products.service import ProductService
from app.infra.cache.redis_service import RedisService
from app.features.products.product import Product
from app.features.products.constants import PRODUCT_CACHE_KEY_TAG
from app.shared.enrichers.product_enricher import ProductEnricher
from app.features.products.mappers.dto_mapper import ProductMapper
from app.features.products.product_dto import ProductDetailDTO

class GetProductByIdUseCase:

    def __init__(
        self,
        product_service: ProductService,
        cache_service: RedisService,
        product_enricher: ProductEnricher
    ):
        self._product_service = product_service
        self._cache_service = cache_service
        self._product_enricher = product_enricher

    async def execute(
        self,
        product_id: int,
    ) -> ProductDetailDTO:

        return await self._cache_service.get_or_set_with_lock_v2(
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
    
    async def _get_product(
        self,
        product_id: int,
    ) -> ProductDetailDTO:

        product = await self._product_service.get_product_entity_by_id(
            product_id
        )

        await self._product_enricher.attach_variant_images(
            [product]
        )

        return ProductMapper.to_product_detail_dto(product)