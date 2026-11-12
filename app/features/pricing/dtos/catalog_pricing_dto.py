from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.features.orders.types.sale import SaleChannel
from app.features.customer.customer_types import CustomerType

from app.features.products.types import CategoryType, BrandType
from app.features.pricing.dtos.cart_pricing_dto import AppliedPromotionDTO

@dataclass
class CatalogPricingItemDTO:
    product_id: int
    category: CategoryType
    brand: BrandType
    unit_price: Decimal

@dataclass
class CatalogPricingContext:
    items: list[CatalogPricingItemDTO]
    sale_channel: SaleChannel
    customer_id: int | None
    customer_type: CustomerType | None
    now: datetime

@dataclass
class CatalogPricingItemResultDTO:
    product_id: int
    original_price: Decimal
    final_price: Decimal
    discount_amount: Decimal

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )

    @property
    def has_discount(self) -> bool:
        return self.discount_amount > 0