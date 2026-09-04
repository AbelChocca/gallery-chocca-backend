from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class CouponDTO:
    id: int

    code: str

    priority: int

    starts_at: datetime

    ends_at: datetime | None

    # pricing_rules: list[PricingRule]

    # conditions: list[PromotionCondition]