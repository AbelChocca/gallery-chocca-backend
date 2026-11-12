from typing import Annotated

from fastapi import Depends

from app.features.pricing.use_cases.get_promotion_detail import (
    GetPromotionDetailUseCase,
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
from app.features.pricing.services.promotion_condition import (
    PromotionConditionService,
)
from app.features.pricing.services.promotion_target import (
    PromotionTargetService,
)
from app.features.pricing.services.coupon import (
    CouponService,
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
from app.features.pricing.dependencies.services.promotion_condition import (
    get_promotion_condition_service,
)
from app.features.pricing.dependencies.services.promotion_target import (
    get_promotion_target_service,
)
from app.features.pricing.dependencies.services.coupon import (
    get_coupon_service,
)


def get_promotion_detail_use_case(
    promotion_service: Annotated[
        PromotionService,
        Depends(get_promotion_service),
    ],
    promotion_pricing_rule_service: Annotated[
        PromotionPricingRuleService,
        Depends(
            get_promotion_pricing_rule_service
        ),
    ],
    promotion_audience_service: Annotated[
        PromotionAudienceService,
        Depends(get_promotion_audience_service),
    ],
    promotion_condition_service: Annotated[
        PromotionConditionService,
        Depends(get_promotion_condition_service),
    ],
    promotion_target_service: Annotated[
        PromotionTargetService,
        Depends(get_promotion_target_service),
    ],
    coupon_service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
) -> GetPromotionDetailUseCase:

    return GetPromotionDetailUseCase(
        promotion_service=promotion_service,
        promotion_pricing_rule_service=(
            promotion_pricing_rule_service
        ),
        promotion_audience_service=(
            promotion_audience_service
        ),
        promotion_condition_service=(
            promotion_condition_service
        ),
        promotion_target_service=(
            promotion_target_service
        ),
        coupon_service=coupon_service,
    )