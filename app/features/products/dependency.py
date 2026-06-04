from app.features.products.service import ProductService

from app.infra.db.uow.unit_of_work import UnitOfWork

from fastapi import Depends
from app.infra.db.uow.dependency import get_uow

from app.infra.cache.dependency import get_cache_service
from app.infra.cache.redis_service import RedisService
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service
from app.shared.slug.slugify_service import SlugService, get_slugify_service
from app.features.media.service import MediaService
from app.features.media.dependency import get_media_service
from app.infra.saga_service import SagaService, get_saga_service

def get_product_service(
    uow: UnitOfWork = Depends(get_uow),
    cache_service: RedisService = Depends(get_cache_service),
    pagination_service: PaginationService = Depends(get_pagination_service),
    media_service: MediaService = Depends(get_media_service),
    saga_service: SagaService = Depends(get_saga_service),
    slug_service: SlugService = Depends(get_slugify_service)
) -> ProductService:
    return ProductService(
        product_repo=uow.products,
        favorite_repo=uow.favorites,
        image_repo=uow.images,
        cart_repo=uow.carts,
        cache_service=cache_service,
        media_service=media_service,
        saga_service=saga_service,
        pagination_service=pagination_service,
        slug_service=slug_service
    )