from datetime import datetime

from app.features.pricing.types.promotion_types import (
    PromotionTargetType,
)


class PromotionTarget:

    def __init__(
        self,
        *,
        id: int | None = None,
        promotion_id: int,
        target_type: PromotionTargetType,
        reference_id: int | None = None,
        reference_value: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.promotion_id = promotion_id
        self.target_type = target_type
        self.reference_id = reference_id
        self.reference_value = reference_value
        self.created_at = created_at