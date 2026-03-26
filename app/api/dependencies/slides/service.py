from app.infra.db.unit_of_work import UnitOfWork

from fastapi import Depends
from app.api.dependencies.uow import get_uow
from app.shared.services.pagination.pagination_service import PaginationService, get_pagination_service
from app.api.dependencies.cache.services import get_cache_service, get_cache_strategy_service
from app.shared.services.cache_strategy.cache_strategy_service import CacheStrategyService
from app.infra.cache.redis_service import RedisService
from app.application.slides.service import SlideService


def get_slide_service(
    uow: UnitOfWork = Depends(get_uow),
    pagination_service: PaginationService = Depends(get_pagination_service),
    cache_service: RedisService = Depends(get_cache_service),
    cache_strategy: CacheStrategyService = Depends(get_cache_strategy_service),
) -> SlideService:

    return SlideService(
        uow.slides,
        uow.images,
        pagination_service,
        cache_service,
        cache_strategy
    )