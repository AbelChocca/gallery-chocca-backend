from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderItem:
    order_id: int

    product_name: str
    sku: str

    quantity: int

    unit_original_price: Decimal
    unit_final_price: Decimal

    original_total: Decimal
    discount_amount: Decimal
    final_total: Decimal

    id: int | None = None

    product_id: int | None = None
    variant_id: int | None = None
    variant_size_id: int | None = None

    color: str | None = None
    size: str | None = None