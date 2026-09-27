from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.features.pricing.types.promotion_types import (
    PromotionTargetType,
)

class CreatePromotionTargetSchema(BaseModel):
    target_type: PromotionTargetType
    reference_id: int | None = None
    reference_value: str | None = None

class PromotionTargetResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    promotion_id: int
    target_type: PromotionTargetType
    reference_id: int | None
    reference_value: str | None
    created_at: datetime | None

class ReplacePromotionTargetsSchema(BaseModel):
    targets: list[CreatePromotionTargetSchema]