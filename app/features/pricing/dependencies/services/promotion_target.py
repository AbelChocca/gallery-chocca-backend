from fastapi import Depends

from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)
from app.infra.db.uow.dependency import (
    get_uow,
)

from app.features.pricing.services.promotion_target import (
    PromotionTargetService,
)


def get_promotion_target_service(
    uow: UnitOfWork = Depends(get_uow),
) -> PromotionTargetService:

    return PromotionTargetService(
        promotion_target_repository=(
            uow.promotion_targets
        ),
    )