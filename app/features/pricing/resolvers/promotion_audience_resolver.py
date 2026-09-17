from app.features.pricing.entities.promotion_audience import PromotionAudience
from app.features.pricing.dtos.promotion_audience_dto import (
    PromotionAudienceContext,
)
from app.features.pricing.types.promotion_types import PromotionAudienceType


class PromotionAudienceResolver:

    def matches_promotion(
        self,
        *,
        audiences: list[PromotionAudience],
        context: PromotionAudienceContext,
    ) -> bool:
        if not audiences:
            return False

        return any(
            self.matches(
                audience=audience,
                context=context,
            )
            for audience in audiences
        )

    def matches(
        self,
        *,
        audience: PromotionAudience,
        context: PromotionAudienceContext,
    ) -> bool:
        if audience.audience_type == PromotionAudienceType.ALL_CUSTOMERS:
            return True

        if audience.audience_type == PromotionAudienceType.CUSTOMER:
            return (
                context.customer_id is not None
                and context.customer_id == audience.reference_id
            )

        if audience.audience_type == PromotionAudienceType.CUSTOMER_GROUP:
            return (
                context.customer_type is not None
                and context.customer_type.value
                == audience.reference_value
            )

        return False