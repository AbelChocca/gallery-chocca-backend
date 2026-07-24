from app.features.products.service import ProductService
from app.features.products.use_cases.create_product import CreateProductUseCase
from app.features.products.use_cases.delete_product import DeleteProductUseCase
from app.features.products.use_cases.update_product import UpdateProductUseCase
from app.features.products.use_cases.get_products import GetProductsUseCase
from app.features.products.use_cases.get_product_by_id import GetProductByIdUseCase
from app.features.products.use_cases.search_product import GetRelatedProductsUseCase

from app.features.inventory.dependencies.services import (
    get_inventory_service,
    get_inventory_movement_service,
)

from app.features.inventory.services.inventory_service import (
    InventoryService,
)

from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)

from app.shared.enrichers.product_enricher import ProductEnricher

from app.shared.pagination.pagination_service import (
    PaginationService,
    get_pagination_service,
)

from app.shared.slug.slugify_service import (
    SlugService,
    get_slugify_service,
)

from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork

from app.infra.cache.dependency import get_cache_service
from app.infra.cache.redis_service import RedisService

from app.features.media.dependency import get_media_service
from app.features.media.service import MediaService

from app.features.favorites.dependency import get_favorite_service
from app.features.favorites.service import FavoriteService

from app.features.cart.dependency import get_cart_service
from app.features.cart.service import CartService

from app.shared.enrichers.dependency import get_product_enricher

from app.infra.saga.saga_service import (
    SagaService,
    get_saga_service,
)

from fastapi import Depends

def get_product_service(
    uow: UnitOfWork = Depends(get_uow),
    slug_service: SlugService = Depends(get_slugify_service)
) -> ProductService:
    return ProductService(
        product_repo=uow.products,
        slug_service=slug_service
    )

def get_create_product_use_case(
    saga_service: SagaService = Depends(get_saga_service),
    product_service: ProductService = Depends(get_product_service),
    media_service: MediaService = Depends(get_media_service),
    cache_service: RedisService = Depends(get_cache_service),
    inventory_service: InventoryService = Depends(
        get_inventory_service
    ),
    inventory_movement_service: InventoryMovementService = Depends(
        get_inventory_movement_service
    ),
) -> CreateProductUseCase:

    return CreateProductUseCase(
        saga_service=saga_service,
        product_service=product_service,
        media_service=media_service,
        cache_service=cache_service,
        inventory_service=inventory_service,
        inventory_movement_service=inventory_movement_service,
    )

def get_update_product_use_case(
    product_service: ProductService = Depends(get_product_service),
    cache_service: RedisService = Depends(get_cache_service),
) -> UpdateProductUseCase:

    return UpdateProductUseCase(
        product_service=product_service,
        cache_service=cache_service,
    )

def get_delete_product_use_case(
    saga_service: SagaService = Depends(get_saga_service),
    product_service: ProductService = Depends(get_product_service),
    media_service: MediaService = Depends(get_media_service),
    favorite_service: FavoriteService = Depends(get_favorite_service),
    cart_service: CartService = Depends(get_cart_service),
    cache_service: RedisService = Depends(get_cache_service),
) -> DeleteProductUseCase:

    return DeleteProductUseCase(
        saga_service=saga_service,
        product_service=product_service,
        media_service=media_service,
        favorite_service=favorite_service,
        cart_service=cart_service,
        cache_service=cache_service,
    )

def get_products_use_case(
    product_service: ProductService = Depends(get_product_service),
    cache_service: RedisService = Depends(get_cache_service),
    pagination_service: PaginationService = Depends(get_pagination_service),
    product_enricher: ProductEnricher = Depends(get_product_enricher),
) -> GetProductsUseCase:

    return GetProductsUseCase(
        product_service=product_service,
        cache_service=cache_service,
        pagination_service=pagination_service,
        product_enricher=product_enricher,
    )

def get_product_by_id_use_case(
    product_service: ProductService = Depends(get_product_service),
    cache_service: RedisService = Depends(get_cache_service),
    product_enricher: ProductEnricher = Depends(get_product_enricher),
) -> GetProductByIdUseCase:

    return GetProductByIdUseCase(
        product_service=product_service,
        cache_service=cache_service,
        product_enricher=product_enricher,
    )

def get_related_products_use_case(
    product_service: ProductService = Depends(get_product_service),
    product_enricher: ProductEnricher = Depends(get_product_enricher),
) -> GetRelatedProductsUseCase:

    return GetRelatedProductsUseCase(
        product_service=product_service,
        product_enricher=product_enricher,
    )