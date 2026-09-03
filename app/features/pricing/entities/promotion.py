from datetime import datetime

from app.features.pricing.types.promotion_types import PromotionStackingMode
from app.features.sales.types.sale import SaleChannel
from app.features.pricing.entities.pricing_rule import PricingRule


class Promotion:

    def __init__(
        self,
        *,
        id: int | None = None,
        name: str,
        description: str | None,
        sales_channel: SaleChannel,
        stacking_mode: PromotionStackingMode,
        priority: int,
        starts_at: datetime | None,
        ends_at: datetime | None,
        is_active: bool,
        pricing_rules: list[PricingRule] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:

        self.id = id

        self.name = name
        self.description = description

        self.sales_channel = sales_channel

        self.stacking_mode = stacking_mode

        self.priority = priority

        self.starts_at = starts_at
        self.ends_at = ends_at

        self.is_active = is_active

        self.pricing_rules = pricing_rules or []
        self.created_at = created_at
        self.updated_at = updated_at