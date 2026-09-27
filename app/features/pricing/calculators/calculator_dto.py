from dataclasses import dataclass, field
from decimal import Decimal

from app.features.pricing.dtos.cart_pricing_dto import AppliedPromotionDTO

@dataclass(frozen=True)
class PricingItemCalculationResult:
    original_unit_price: Decimal
    final_unit_price: Decimal
    original_total: Decimal
    final_total: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )

@dataclass(frozen=True)
class PricingSubtotalCalculationResult:
    original_subtotal: Decimal
    final_subtotal: Decimal
    discount_amount: Decimal
    applied_promotions: list[AppliedPromotionDTO]