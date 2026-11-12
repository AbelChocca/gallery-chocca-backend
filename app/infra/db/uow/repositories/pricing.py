from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
)
from app.features.pricing.models.model_promotion import (
    PromotionTable,
)
from app.features.pricing.mappers.promotion_mapper import (
    PromotionMapper,
)

from app.features.pricing.repositories.pricing_rule_repository import (
    PricingRuleRepository,
)
from app.features.pricing.models.model_pricing_rule import (
    PricingRuleTable,
)
from app.features.pricing.mappers.pricing_rule_mapper import (
    PricingRuleMapper,
)

from app.features.pricing.repositories.promotion_audience_repository import (
    PromotionAudienceRepository,
)
from app.features.pricing.models.promotion_audience import (
    PromotionAudienceTable,
)
from app.features.pricing.mappers.promotion_audience_mapper import (
    PromotionAudienceMapper,
)

from app.features.pricing.repositories.promotion_target_repository import (
    PromotionTargetRepository,
)
from app.features.pricing.models.promotion_target import (
    PromotionTargetTable,
)
from app.features.pricing.mappers.promotion_target_mapper import (
    PromotionTargetMapper,
)

from app.features.pricing.repositories.promotion_condition_repository import (
    PromotionConditionRepository,
)
from app.features.pricing.models.promotion_condition import (
    PromotionConditionTable,
)
from app.features.pricing.mappers.promotion_condition_mapper import (
    PromotionConditionMapper,
)

from app.features.pricing.repositories.promotion_pricing_rule_repository import (
    PromotionPricingRuleRepository,
)
from app.features.pricing.repositories.coupon_repsitory import (
    CouponRepository,
)
from app.features.pricing.models.coupon import (
    CouponTable,
)
from app.features.pricing.mappers.coupon_mapper import (
    CouponMapper,
)
from app.features.pricing.repositories.coupon_redemption_repository import (
    CouponRedemptionRepository,
)
from app.features.pricing.models.coupon_redemption import (
    CouponRedemptionTable,
)
from app.features.pricing.mappers.coupon_redemption_mapper import (
    CouponRedemptionMapper,
)

class PricingRepositoriesMixin:

    @property
    def promotions(
        self,
    ) -> PromotionRepository:
        return self._get_or_create(
            "promotions",
            lambda: PromotionRepository(
                self.session,
                PromotionMapper,
                PromotionTable,
            ),
        )

    @property
    def coupons(
        self,
    ) -> CouponRepository:
        return self._get_or_create(
            "coupons",
            lambda: CouponRepository(
                self.session,
                CouponMapper,
                CouponTable,
            ),
        )

    @property
    def coupon_redemptions(
        self,
    ) -> CouponRedemptionRepository:
        return self._get_or_create(
            "coupon_redemptions",
            lambda: CouponRedemptionRepository(
                self.session,
                CouponRedemptionMapper,
                CouponRedemptionTable,
            ),
        )

    @property
    def pricing_rules(
        self,
    ) -> PricingRuleRepository:
        return self._get_or_create(
            "pricing_rules",
            lambda: PricingRuleRepository(
                self.session,
                PricingRuleMapper,
                PricingRuleTable,
            ),
        )

    @property
    def promotion_audiences(
        self,
    ) -> PromotionAudienceRepository:
        return self._get_or_create(
            "promotion_audiences",
            lambda: PromotionAudienceRepository(
                self.session,
                PromotionAudienceMapper,
                PromotionAudienceTable,
            ),
        )

    @property
    def promotion_targets(
        self,
    ) -> PromotionTargetRepository:
        return self._get_or_create(
            "promotion_targets",
            lambda: PromotionTargetRepository(
                self.session,
                PromotionTargetMapper,
                PromotionTargetTable,
            ),
        )

    @property
    def promotion_conditions(
        self,
    ) -> PromotionConditionRepository:
        return self._get_or_create(
            "promotion_conditions",
            lambda: PromotionConditionRepository(
                self.session,
                PromotionConditionMapper,
                PromotionConditionTable,
            ),
        )

    @property
    def promotion_pricing_rules(
        self,
    ) -> PromotionPricingRuleRepository:
        return self._get_or_create(
            "promotion_pricing_rules",
            lambda: PromotionPricingRuleRepository(
                db_session=self.session,
            ),
        )