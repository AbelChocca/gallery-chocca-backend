from enum import Enum
from typing import TypedDict
from decimal import Decimal

class CartStatus(str, Enum):
    ACTIVE = "active"
    ABANDONED = "abandoned"
    CONVERTED = "converted"

class CartItemRow(TypedDict):
    cart_item_id: int

    product_id: int
    nombre: str
    base_price: Decimal
    is_product_active: bool
    subtotal: Decimal
    final_subtotal: Decimal
    final_price: Decimal

    variant_id: int
    color: str

    variant_size_id: int
    size: str
    stock: int
    sku: str

    has_stock: bool
    available_quantity: int
    is_available: bool

    image_url: str | None

    quantity: int