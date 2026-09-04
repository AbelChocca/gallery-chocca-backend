from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.sales.types.payment import PaymentMethod
from app.features.sales.types.sale import SaleChannel
from app.features.products.types import CategoryType, BrandType

@dataclass(slots=True)
class PricingItemResultDTO:

    product_id: int

    quantity: int

    original_unit_price: Decimal

    final_unit_price: Decimal

    original_total: Decimal

    final_total: Decimal

    discount_amount: Decimal

@dataclass(slots=True)
class SalePricingDTO:

    items: list[PricingItemResultDTO]

    subtotal: Decimal

    discount_amount: Decimal

    shipping_cost: Decimal

    total: Decimal

@dataclass(slots=True)
class PricingItemDTO:
    product_id: int
    quantity: int
    category: CategoryType
    brand: BrandType
    unit_price: Decimal


@dataclass(slots=True)
class SalePricingContext:
    items: list[PricingItemDTO]

    sale_channel: SaleChannel

    customer_id: int | None = None
    payment_method: PaymentMethod | None = None
    coupon_code: str | None = None

    now: datetime
    shipping_cost: Decimal = Decimal("0")
