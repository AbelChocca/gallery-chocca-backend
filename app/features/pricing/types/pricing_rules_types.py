from enum import Enum
from typing import TypedDict
from decimal import Decimal

class PricingRuleType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    FIXED_AMOUNT = "FIXED_AMOUNT"
    FIXED_PRICE = "FIXED_PRICE"

    BUY_X_GET_Y = "BUY_X_GET_Y"

    FREE_ITEM = "FREE_ITEM"

    FREE_SHIPPING = "FREE_SHIPPING"

class ProductPricingSummaryTD(TypedDict):
    id: int
    nombre: str
    categoria: str

    image_url: str | None

    base_price: Decimal
    is_active: bool

    final_price: Decimal