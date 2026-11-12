from fastapi import Depends

from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)
from app.infra.db.uow.dependency import (
    get_uow,
)

from app.features.pricing.services.promotion import (
    PromotionService,
)
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service


def get_promotion_service(
    uow: UnitOfWork = Depends(get_uow),
    pagination_service: PaginationService = Depends(get_pagination_service)
) -> PromotionService:

    return PromotionService(
        promotion_repository=uow.promotions,
        pagination_service=pagination_service
    )