from fastapi import Depends

from app.features.pricing.use_cases.create_promotion import (
    CreatePromotionUseCase,
)

from app.features.pricing.services.promotion import (
    PromotionService,
)
from app.features.pricing.services.promotion_pricing_rule import (
    PromotionPricingRuleService,
)
from app.features.pricing.services.promotion_audience import (
    PromotionAudienceService,
)
from app.features.pricing.services.promotion_target import (
    PromotionTargetService,
)
from app.features.pricing.services.promotion_condition import (
    PromotionConditionService,
)

from app.features.pricing.dependencies.services.promotion import (
    get_promotion_service,
)
from app.features.pricing.dependencies.services.promotion_pricing_rule import (
    get_promotion_pricing_rule_service,
)
from app.features.pricing.dependencies.services.promotion_audience import (
    get_promotion_audience_service,
)
from app.features.pricing.dependencies.services.promotion_target import (
    get_promotion_target_service,
)
from app.features.pricing.dependencies.services.promotion_condition import (
    get_promotion_condition_service,
)


def get_create_promotion_use_case(
    promotion_service: PromotionService = Depends(
        get_promotion_service
    ),
    promotion_pricing_rule_service: PromotionPricingRuleService = Depends(
        get_promotion_pricing_rule_service
    ),
    promotion_audience_service: PromotionAudienceService = Depends(
        get_promotion_audience_service
    ),
    promotion_target_service: PromotionTargetService = Depends(
        get_promotion_target_service
    ),
    promotion_condition_service: PromotionConditionService = Depends(
        get_promotion_condition_service
    ),
) -> CreatePromotionUseCase:

    return CreatePromotionUseCase(
        promotion_service=promotion_service,
        promotion_pricing_rule_service=(
            promotion_pricing_rule_service
        ),
        promotion_audience_service=(
            promotion_audience_service
        ),
        promotion_target_service=(
            promotion_target_service
        ),
        promotion_condition_service=(
            promotion_condition_service
        ),
    )