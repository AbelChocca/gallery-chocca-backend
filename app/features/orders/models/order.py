from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, Enum as SQLEnum, DateTime, Sequence
from sqlmodel import Field, SQLModel

from app.features.orders.types.order import OrderStatus
from app.features.payments.types.payment import PaymentMethod

order_number_sequence = Sequence(
    "order_number_seq",
    start=1,
    increment=1,
)

class OrderTable(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    order_number: str = Field(
        max_length=30,
        nullable=False,
        unique=True,
        index=True,
    )

    customer_id: int | None = Field(
        default=None,
        foreign_key="customer.id",
        nullable=True,
        index=True,
    )

    payment_method: PaymentMethod = Field(
        sa_column=Column(
            SQLEnum(
                PaymentMethod,
                values_callable=lambda enum: [
                    e.value for e in enum
                ],
                native_enum=False,
                create_constraint=True,
                name="ck_orders_payment_method",
            ),
            nullable=False,
        ),
    )

    status: OrderStatus = Field(
        default=OrderStatus.PENDING_PAYMENT,
        sa_column=Column(
            SQLEnum(
                OrderStatus,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
                name="ck_orders_status",
            ),
            nullable=False,
            server_default=OrderStatus.PENDING_PAYMENT.value,
        ),
    )

    subtotal: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    discount_amount: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    shipping_cost: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    total: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )