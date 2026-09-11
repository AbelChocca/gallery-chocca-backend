from dataclasses import dataclass, field
from datetime import datetime

from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.entities.promotion_audience import PromotionAudience
from app.features.pricing.types.promotion_types import PromotionStackingMode
from app.features.pricing.entities.promotion_condition import PromotionCondition
from app.features.pricing.entities.coupon import Coupon
from app.features.pricing.entities.promotion_target import PromotionTarget
from app.features.sales.types.sale import SaleChannel


@dataclass
class Promotion:
    id: int | None
    name: str
    description: str | None
    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    priority: int
    starts_at: datetime | None
    ends_at: datetime | None
    is_active: bool
    pricing_rules: list[PricingRule] = field(default_factory=list)
    audiences: list[PromotionAudience] = field(default_factory=list)
    conditions: list[PromotionCondition] = field(default_factory=list)
    coupons: list[Coupon] = field(default_factory=list)
    targets: list[PromotionTarget] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None