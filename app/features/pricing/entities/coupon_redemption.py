from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class CouponRedemption:
    id: int | None
    coupon_id: int
    customer_id: int
    created_at: datetime | None