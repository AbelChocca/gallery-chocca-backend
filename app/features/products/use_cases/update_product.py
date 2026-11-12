from app.features.products.service import ProductService
from app.infra.cache.redis_service import RedisService

from app.features.products.constants import PRODUCT_CACHE_KEY_TAG

from app.features.products.types import BrandType, CategoryType
from decimal import Decimal

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
        *,
        product_id: int,
        nombre: str | None = None,
        descripcion: str | None = None,
        brand: BrandType | None = None,
        category: CategoryType | None = None,
        fit: str | None = None,
        base_price: Decimal | None = None,
    ) -> None:
        await self._product_service.update_product(
            product_id=product_id,
            nombre=nombre,
            descripcion=descripcion,
            brand=brand,
            category=category,
            fit=fit,
            base_price=base_price,
        )

        await self._cache_service.invalidate_entity(
            PRODUCT_CACHE_KEY_TAG,
            product_id,
        )
        await self._cache_service.invalidate_entities(
            PRODUCT_CACHE_KEY_TAG,
        )