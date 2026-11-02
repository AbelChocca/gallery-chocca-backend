from dataclasses import dataclass
from decimal import Decimal

from app.features.pricing.types.promotion_types import (
    PromotionApplicationScope,
)


@dataclass(frozen=True, slots=True)
class AdminOrderPromotionDTO:
    id: int

    promotion_id: int | None

    name: str

    application_scope: PromotionApplicationScope

    coupon_code: str | None

    discount_amount: Decimal

@dataclass(frozen=True, slots=True)
class MyOrderPromotionDTO:
    id: int

    promotion_id: int | None

    name: str

    application_scope: PromotionApplicationScope

    coupon_code: str | None

    discount_amount: Decimal