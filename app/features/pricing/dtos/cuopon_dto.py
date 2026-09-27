from dataclasses import dataclass
from datetime import datetime

from app.features.pricing.types.promotion_types import PromotionStackingMode
from app.features.sales.types.sale import SaleChannel

@dataclass(slots=True)
class CouponPromotionDTO:
    id: int
    name: str
    description: str | None
    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    priority: int
    is_active: bool

@dataclass(slots=True)
class CouponDetailDTO:
    id: int
    promotion_id: int
    code: str
    is_active: bool

    starts_at: datetime | None
    ends_at: datetime | None

    max_redemptions: int | None
    max_redemptions_per_customer: int | None

    used_count: int

    promotion: CouponPromotionDTO

    created_at: datetime | None
    updated_at: datetime | None