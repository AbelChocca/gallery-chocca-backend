from dataclasses import dataclass
from decimal import Decimal

from app.features.pricing.entities.product_applied_pricing_rule import ProductAppliedPricingRule

@dataclass
class PricingCalculationResult:
    final_price: Decimal
    applied_rules: list[ProductAppliedPricingRule]
    latest_applied_rule: ProductAppliedPricingRule | None