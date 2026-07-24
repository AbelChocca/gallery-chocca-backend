from app.features.products.service import ProductService
from app.infra.cache.redis_service import RedisService

from app.features.products.product_dto import UpdateProductCommand
from app.features.products.constants import PRODUCT_CACHE_KEY_TAG


class UpdateProductUseCase:

    def __init__(
        self,
        product_service: ProductService,
        cache_service: RedisService,
    ):
        self._product_service = product_service
        self._cache_service = cache_service


    async def execute(
        self,
        product_id: int,
        command: UpdateProductCommand
    ):
        product = await self._product_service.update_product(
            product_id,
            command
        )


        await self._cache_service.invalidate_entity(
            PRODUCT_CACHE_KEY_TAG,
            product_id
        )


        await self._cache_service.invalidate_entities(
            PRODUCT_CACHE_KEY_TAG
        )


        return {
            "id": product.id,
            "slug": product.slug
        }