from dataclasses import dataclass
from decimal import Decimal

from app.features.pricing.entities.product_applied_pricing_rule import ProductAppliedPricingRule

@dataclass
class PricingCalculationResult:
    final_price: Decimal
    applied_rules: list[ProductAppliedPricingRule]
    latest_applied_rule: ProductAppliedPricingRule | None

@dataclass(frozen=True)
class PricingItemCalculationResult:
    original_unit_price: Decimal
    final_unit_price: Decimal
    original_total: Decimal
    final_total: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal