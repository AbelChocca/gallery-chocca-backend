from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class AdminOrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    product_id: int | None
    variant_id: int | None
    variant_size_id: int | None

    product_name: str
    sku: str

    color: str | None
    size: str | None

    quantity: int

    unit_original_price: Decimal
    unit_final_price: Decimal

    discount_amount: Decimal

    original_total: Decimal
    final_total: Decimal

class MyOrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    product_id: int | None
    variant_id: int | None
    variant_size_id: int | None

    product_name: str
    sku: str

    color: str | None
    size: str | None

    quantity: int

    unit_original_price: Decimal
    unit_final_price: Decimal

    discount_amount: Decimal

    original_total: Decimal
    final_total: Decimal