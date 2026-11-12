from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.features.orders.types.sale import SaleChannel
from app.features.customer.customer_types import CustomerType
from app.features.products.types import CategoryType, BrandType
from app.features.orders.types.order_promotion import PromotionApplicationScope

@dataclass
class CartPricingItemDTO:
    item_id: int

    product_id: int
    category: CategoryType
    brand: BrandType

    quantity: int
    unit_price: Decimal


@dataclass
class CartPricingContext:
    items: list[CartPricingItemDTO]
    sale_channel: SaleChannel
    customer_id: int | None
    customer_type: CustomerType | None
    now: datetime

@dataclass(frozen=True)
class AppliedPromotionDTO:
    promotion_id: int
    name: str
    discount_amount: Decimal

    application_scope: PromotionApplicationScope | None = None
    coupon_code: str | None = None

@dataclass
class CartPricingItemResultDTO:
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


@dataclass
class CartPricingDTO:
    items: list[CartPricingItemResultDTO]
    subtotal: Decimal
    discount_amount: Decimal
    total: Decimal

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )