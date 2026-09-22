from fastapi import Depends

from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)
from app.infra.db.uow.dependency import (
    get_uow,
)

from app.features.pricing.services.promotion_pricing_rule import (
    PromotionPricingRuleService,
)


def get_promotion_pricing_rule_service(
    uow: UnitOfWork = Depends(get_uow),
) -> PromotionPricingRuleService:

    return PromotionPricingRuleService(
        pricing_rule_repository=uow.pricing_rules,
        promotion_pricing_rule_repository=(
            uow.promotion_pricing_rules
        ),
    )