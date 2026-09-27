from enum import Enum
from dataclasses import dataclass
from decimal import Decimal

class PricingRuleType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    FIXED_AMOUNT = "FIXED_AMOUNT"
    FIXED_PRICE = "FIXED_PRICE"

    BUY_X_GET_Y = "BUY_X_GET_Y"

    FREE_ITEM = "FREE_ITEM"

    FREE_SHIPPING = "FREE_SHIPPING"

@dataclass
class PricingStrategyResult:
    unit_price: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal