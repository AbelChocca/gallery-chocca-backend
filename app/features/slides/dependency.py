from app.infra.db.uow.unit_of_work import UnitOfWork

from fastapi import Depends
from app.infra.db.uow.dependency import get_uow
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service
from app.infra.cache.dependency import get_cache_service
from app.infra.cache.redis_service import RedisService
from app.features.slides.service import SlideService
from app.features.media.service import MediaService
from app.features.media.dependency import get_media_service
from app.infra.saga_service import SagaService, get_saga_service

def get_slide_service(
    uow: UnitOfWork = Depends(get_uow),
    pagination_service: PaginationService = Depends(get_pagination_service),
    cache_service: RedisService = Depends(get_cache_service),
    media_service: MediaService = Depends(get_media_service),
    saga_service: SagaService = Depends(get_saga_service)
) -> SlideService:

    return SlideService(
        slide_repo=uow.slides,
        image_repo=uow.images,
        media_service=media_service,
        saga_service=saga_service,
        pagination_service=pagination_service,
        cache_service=cache_service
    )