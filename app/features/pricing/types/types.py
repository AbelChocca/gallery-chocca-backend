from enum import Enum
from typing import TypedDict, TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from app.features.pricing.entities.product_applied_pricing_rule import (
        ProductAppliedPricingRule
    )

class PricingRuleType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"
    FINAL_PRICE = "FINAL_PRICE"

class ProductPricingSummaryTD(TypedDict):
    id: int
    nombre: str
    categoria: str

    image_url: str | None

    base_price: Decimal
    is_active: bool
    latest_applied_rule: "ProductAppliedPricingRule"

    final_price: Decimal