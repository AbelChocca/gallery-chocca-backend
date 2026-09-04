from datetime import datetime

from app.features.pricing.entities.pricing_rule import PricingRule

class ProductAppliedPricingRule:
    def __init__(
        self,
        *,
        product_id: int,
        pricing_rule: PricingRule,
        assigned_at: datetime
    ):
        self.product_id = product_id
        self.pricing_rule = pricing_rule
        self.assigned_at = assigned_at