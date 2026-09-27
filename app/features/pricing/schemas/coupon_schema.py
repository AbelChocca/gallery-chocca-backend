from datetime import datetime

from pydantic import BaseModel, ConfigDict
from app.features.pricing.types.promotion_types import (
    PromotionStackingMode,
)
from app.features.sales.types.sale import SaleChannel


class CreateCouponSchema(BaseModel):
    promotion_id: int
    code: str

    is_active: bool = True

    starts_at: datetime | None = None
    ends_at: datetime | None = None

    max_redemptions: int | None = None
    max_redemptions_per_customer: int | None = None


class CouponResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    
    id: int
    promotion_id: int
    code: str
    is_active: bool
    starts_at: datetime | None
    ends_at: datetime | None
    max_redemptions: int | None
    max_redemptions_per_customer: int | None
    used_count: int
    created_at: datetime | None
    updated_at: datetime | None

class UpdateCouponSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    code: str | None = None
    is_active: bool | None = None

    starts_at: datetime | None = None
    ends_at: datetime | None = None

    max_redemptions: int | None = None
    max_redemptions_per_customer: int | None = None

class CouponRedemptionResponseSchema(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    coupon_id: int
    customer_id: int
    created_at: datetime

class CouponPromotionResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    description: str | None

    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode

    priority: int
    is_active: bool

class CouponDetailResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    promotion_id: int

    code: str
    is_active: bool

    starts_at: datetime | None
    ends_at: datetime | None

    max_redemptions: int | None
    max_redemptions_per_customer: int | None

    used_count: int

    promotion: CouponPromotionResponseSchema

    created_at: datetime | None
    updated_at: datetime | None