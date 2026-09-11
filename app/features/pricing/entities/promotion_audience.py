from dataclasses import dataclass
from datetime import datetime

from app.features.pricing.types.promotion_types import PromotionAudienceType


@dataclass(slots=True)
class PromotionAudience:
    id: int | None
    promotion_id: int
    audience_type: PromotionAudienceType
    reference_id: int | None
    reference_value: str | None
    created_at: datetime