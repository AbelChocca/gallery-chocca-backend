from dataclasses import dataclass

from app.features.pricing.types.promotion_types import (
    PromotionTargetType,
)


@dataclass(frozen=True)
class PromotionTargetAssignment:
    target_type: PromotionTargetType
    reference_id: int | None = None
    reference_value: str | None = None