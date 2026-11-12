from app.features.pricing.entities.promotion import (
    Promotion,
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


class GetPromotionDetailUseCase:

    def __init__(
        self,
        *,
        promotion_service: PromotionService,
        promotion_pricing_rule_service: PromotionPricingRuleService,
        promotion_audience_service: PromotionAudienceService,
        promotion_condition_service: PromotionConditionService,
        promotion_target_service: PromotionTargetService,
        coupon_service: CouponService,
    ) -> None:

        self._promotion_service = (
            promotion_service
        )

        self._promotion_pricing_rule_service = (
            promotion_pricing_rule_service
        )

        self._promotion_audience_service = (
            promotion_audience_service
        )

        self._promotion_condition_service = (
            promotion_condition_service
        )

        self._promotion_target_service = (
            promotion_target_service
        )

        self._coupon_service = (
            coupon_service
        )

    async def execute(
        self,
        *,
        promotion_id: int,
    ) -> Promotion:

        promotion = await self._promotion_service.get_by_id(
            promotion_id=promotion_id,
        )

        promotion.pricing_rules = (
            await self
            ._promotion_pricing_rule_service
            .get_by_promotion(
                promotion_id=promotion_id,
            )
        )

        promotion.audiences = (
            await self
            ._promotion_audience_service
            .get_by_promotion(
                promotion_id=promotion_id,
            )
        )

        promotion.conditions = (
            await self
            ._promotion_condition_service
            .get_by_promotion(
                promotion_id=promotion_id,
            )
        )

        promotion.targets = (
            await self
            ._promotion_target_service
            .get_by_promotion(
                promotion_id=promotion_id,
            )
        )

        promotion.coupons = (
            await self
            ._coupon_service
            .get_by_promotion(
                promotion_id=promotion_id,
            )
        )

        return promotion