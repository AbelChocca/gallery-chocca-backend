from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.orders.types.order import OrderStatus
from app.features.payments.types.payment import PaymentMethod

@dataclass
class Order:

    order_number: str
    customer_id: int | None

    status: OrderStatus
    payment_method: PaymentMethod

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def generate_order_number(
        sequence: int,
        created_at: datetime,
    ) -> str:
        return f"GC-{created_at.year}-{sequence:06d}"