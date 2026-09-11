from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.features.pricing.types.promotion_types import (
    PromotionConditionType,
)


@dataclass(slots=True)
class PromotionCondition:
    id: int | None
    promotion_id: int
    condition_type: PromotionConditionType
    parameters: dict[str, Any]
    description: str | None
    created_at: datetime