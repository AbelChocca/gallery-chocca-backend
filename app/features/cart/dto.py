from dataclasses import dataclass, field
from decimal import Decimal

from app.features.products.types import (
    CategoryType,
    BrandType,
)
from app.features.pricing.dtos.cart_pricing_dto import AppliedPromotionDTO

@dataclass(frozen=True, slots=True)
class CartItemRow:
    cart_item_id: int

    product_id: int
    nombre: str
    category: CategoryType
    brand: BrandType
    base_price: Decimal
    is_product_active: bool

    variant_id: int
    color: str

    variant_size_id: int
    size: str
    stock: int
    sku: str

    has_stock: bool

    image_url: str | None

    quantity: int

@dataclass(slots=True)
class CartItemDTO:
    cart_item_id: int

    product_id: int
    nombre: str

    variant_id: int
    color: str

    variant_size_id: int
    size: str
    sku: str

    quantity: int
    stock: int
    has_stock: bool
    is_product_active: bool

    image_url: str | None

    original_price: Decimal
    final_price: Decimal
    discount_amount: Decimal
    has_discount: bool

    original_total: Decimal
    final_total: Decimal

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )

@dataclass(slots=True)
class FullCartDTO:
    cart_id: int
    items: list[CartItemDTO]

    subtotal: Decimal
    discount_amount: Decimal
    total: Decimal

    total_items: int

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )
