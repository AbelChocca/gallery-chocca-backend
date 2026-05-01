from app.application.products.service import ProductService

from app.infra.db.unit_of_work import UnitOfWork

from fastapi import Depends
from app.api.dependencies.uow import get_uow

from app.api.dependencies.cache.services import get_cache_service
from app.infra.cache.redis_service import RedisService
from app.shared.services.pagination.pagination_service import PaginationService, get_pagination_service
from app.shared.services.slug.slugify_service import SlugService, get_slugify_service

def get_product_service(
    uow: UnitOfWork = Depends(get_uow),
    cache_service: RedisService = Depends(get_cache_service),
    pagination_service: PaginationService = Depends(get_pagination_service),
    slug_service: SlugService = Depends(get_slugify_service)
) -> ProductService:
    return ProductService(
        product_repo=uow.products,
        favorite_repo=uow.favorites,
        image_repo=uow.images,
        cache_service=cache_service,
        pagination_service=pagination_service,
        slug_service=slug_service
    )