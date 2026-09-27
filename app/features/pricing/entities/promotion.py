from dataclasses import dataclass, field
from datetime import datetime

from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.entities.promotion_audience import PromotionAudience
from app.features.pricing.types.promotion_types import PromotionStackingMode, PromotionApplicationScope
from app.features.pricing.entities.promotion_condition import PromotionCondition
from app.features.pricing.entities.coupon import Coupon
from app.features.pricing.entities.promotion_target import PromotionTarget
from app.features.sales.types.sale import SaleChannel
from app.core.exceptions import ValidationError

@dataclass
class Promotion:
    id: int | None
    name: str
    description: str | None
    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    application_scope: PromotionApplicationScope
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

    def validate(self) -> None:
        if not self.name.strip():
            raise ValidationError(
                "El nombre de la promocion no puede estar vacia."
            )

        if self.priority < 0:
            raise ValidationError(
                "La prioridad de la promocion no puede ser negativa."
            )

        if (
            self.starts_at is not None
            and self.ends_at is not None
            and self.ends_at <= self.starts_at
        ):
            raise ValidationError(
                "La fecha de fin de la promocion debe ser mayor que su fecha de comienzo."
            )