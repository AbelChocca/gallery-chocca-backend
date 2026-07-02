from datetime import datetime


class ProductPricingRule:
    def __init__(
        self,
        product_id: int,
        pricing_rule_id: int,
        assigned_at: datetime | None = None,
    ):
        self.product_id = product_id
        self.pricing_rule_id = pricing_rule_id
        self.assigned_at = assigned_at