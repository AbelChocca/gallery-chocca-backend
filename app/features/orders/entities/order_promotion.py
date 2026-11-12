from dataclasses import dataclass
from decimal import Decimal

from app.features.pricing.types.promotion_types import PromotionApplicationScope


@dataclass
class OrderPromotion:
    order_id: int

    name: str
    application_scope: PromotionApplicationScope

    discount_amount: Decimal

    promotion_id: int | None = None
    coupon_code: str | None = None
    id: int | None = None