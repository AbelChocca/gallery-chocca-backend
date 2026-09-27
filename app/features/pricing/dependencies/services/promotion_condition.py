from fastapi import Depends

from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)
from app.infra.db.uow.dependency import (
    get_uow,
)

from app.features.pricing.services.promotion_condition import (
    PromotionConditionService,
)


def get_promotion_condition_service(
    uow: UnitOfWork = Depends(get_uow),
) -> PromotionConditionService:

    return PromotionConditionService(
        promotion_condition_repository=(
            uow.promotion_conditions
        ),
    )