from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.features.pricing.types.promotion_types import (
    PromotionApplicationScope,
)

class AdminOrderPromotionResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    promotion_id: int | None

    name: str

    application_scope: PromotionApplicationScope

    coupon_code: str | None

    discount_amount: Decimal

class MyOrderPromotionResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    promotion_id: int | None

    name: str

    application_scope: PromotionApplicationScope

    coupon_code: str | None

    discount_amount: Decimal