from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.features.payments.types.payment_legacy import PaymentMethod
from app.features.orders.types.sale import SaleChannel
from app.features.products.types import CategoryType, BrandType
from app.features.customer.customer_types import CustomerType
from app.features.pricing.dtos.cart_pricing_dto import AppliedPromotionDTO

@dataclass(slots=True)
class PricingItemResultDTO:
    item_id: int
    product_id: int
    quantity: int

    original_unit_price: Decimal
    final_unit_price: Decimal

    original_total: Decimal
    final_total: Decimal
    discount_amount: Decimal

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )

    @property
    def has_discount(self) -> bool:
        return self.discount_amount > 0

@dataclass(slots=True)
class SalePricingDTO:
    items: list[PricingItemResultDTO]

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )

@dataclass(slots=True)
class PricingItemDTO:
    item_id: int
    product_id: int
    category: CategoryType
    brand: BrandType
    quantity: int
    unit_price: Decimal


@dataclass(slots=True)
class SalePricingContext:
    items: list[PricingItemDTO]

    sale_channel: SaleChannel

    now: datetime

    shipping_cost: Decimal = Decimal("0.00")

    customer_id: int | None = None
    customer_type: CustomerType | None = None

    payment_method: PaymentMethod | None = None

    coupon_code: str | None = None
