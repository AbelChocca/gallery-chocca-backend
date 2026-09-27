from dataclasses import dataclass

from app.features.sales.types.customer import CustomerType
from app.features.pricing.types.promotion_types import (
    PromotionAudienceType,
)


@dataclass(frozen=True)
class PromotionAudienceContext:
    customer_id: int | None = None
    customer_type: CustomerType | None = None

@dataclass(frozen=True)
class PromotionAudienceAssignment:
    audience_type: PromotionAudienceType
    reference_id: int | None = None
    reference_value: str | None = None

@dataclass(slots=True)
class CreatePromotionAudienceDTO:
    audience_type: PromotionAudienceType
    reference_id: int | None = None
    reference_value: str | None = None