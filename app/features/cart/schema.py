from pydantic import BaseModel, Field
from decimal import Decimal

class AddCartItemRequest(BaseModel):
    product_id: int
    variant_id: int
    variant_size_id: int
    quantity: int = Field(gt=0, default=1)

class CartItemRow(BaseModel):
    cart_item_id: int

    product_id: int
    nombre: str
    base_price: Decimal
    is_product_active: bool
    final_price: Decimal
    final_subtotal: Decimal
    subtotal: Decimal

    variant_id: int
    color: str

    variant_size_id: int
    size: str
    stock: int
    sku: str

    has_stock: bool
    available_quantity: int
    is_available: bool

    image_url: str = None

    quantity: int

class CartResponse(BaseModel):
    cart_id: int | None

    items: list[CartItemRow]

    subtotal: Decimal
    total: Decimal
    total_items: int