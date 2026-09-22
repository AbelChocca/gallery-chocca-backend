from fastapi import Depends

from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)
from app.infra.db.uow.dependency import (
    get_uow,
)

from app.features.pricing.services.promotion_audience import (
    PromotionAudienceService,
)


def get_promotion_audience_service(
    uow: UnitOfWork = Depends(get_uow),
) -> PromotionAudienceService:

    return PromotionAudienceService(
        promotion_audience_repository=(
            uow.promotion_audiences
        ),
    )