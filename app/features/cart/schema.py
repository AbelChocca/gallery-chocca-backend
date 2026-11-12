from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

from app.features.pricing.schemas.promotion_schema import AppliedPromotionResponseSchema

class AddCartItemRequest(BaseModel):
    product_id: int
    variant_id: int
    variant_size_id: int
    quantity: int = Field(gt=0, default=1)

class CartItemResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

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

    applied_promotions: list[
        AppliedPromotionResponseSchema
    ]


class GetFullCartResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    cart_id: int
    items: list[CartItemResponseSchema]

    subtotal: Decimal
    discount_amount: Decimal
    total: Decimal

    total_items: int

    applied_promotions: list[
        AppliedPromotionResponseSchema
    ] 