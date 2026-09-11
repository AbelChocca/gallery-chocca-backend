from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Coupon:
    id: int | None
    promotion_id: int
    code: str
    is_active: bool
    starts_at: datetime | None
    ends_at: datetime | None
    max_redemptions: int | None
    max_redemptions_per_customer: int | None
    used_count: int
    created_at: datetime
    updated_at: datetime