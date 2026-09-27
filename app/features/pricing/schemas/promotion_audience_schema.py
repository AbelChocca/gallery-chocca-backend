from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.features.pricing.types.promotion_types import (
    PromotionAudienceType
)


class CreatePromotionAudienceSchema(BaseModel):
    audience_type: PromotionAudienceType
    reference_id: int | None = None
    reference_value: str | None = None

class PromotionAudienceResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    promotion_id: int
    audience_type: PromotionAudienceType
    reference_id: int | None
    reference_value: str | None
    created_at: datetime | None

class ReplacePromotionAudiencesSchema(BaseModel):
    audiences: list[CreatePromotionAudienceSchema]
