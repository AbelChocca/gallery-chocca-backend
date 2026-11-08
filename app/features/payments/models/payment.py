from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, Enum as SQLEnum, Numeric, DateTime
from sqlmodel import Field, SQLModel

from app.features.payments.types.payment import PaymentStatus, PaymentMethod
from app.features.payments.types.payment_provider import PaymentProvider


class PaymentTable(SQLModel, table=True):
    __tablename__ = "payments"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    order_id: int = Field(
        foreign_key="orders.id",
        nullable=False,
        index=True,
    )

    provider: PaymentProvider = Field(
        sa_column=Column(
            SQLEnum(
                PaymentProvider,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
                name="ck_payments_provider",
            ),
            nullable=False,
        ),
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
                name="ck_payments_payment_method",
            ),
            nullable=False,
        ),
    )

    status: PaymentStatus = Field(
        sa_column=Column(
            SQLEnum(
                PaymentStatus,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
                name="ck_payments_status",
            ),
            nullable=False,
        ),
    )

    amount: Decimal = Field(
        sa_column=Column(
            Numeric(12, 2),
            nullable=False,
        ),
    )

    currency: str = Field(
        default="PEN",
        max_length=3,
        nullable=False,
    )

    provider_payment_id: str | None = Field(
        default=None,
        max_length=45,
        nullable=True,
        unique=True,
        index=True,
    )

    provider_order_id: str = Field(
        max_length=100,
        nullable=False,
        unique=True,
        index=True,
    )

    authorization: str | None = Field(
        default=None,
        max_length=100,
        nullable=True,
    )

    error_code: str | None = Field(
        default=None,
        max_length=50,
        nullable=True,
    )

    error_message: str | None = Field(
        default=None,
        max_length=500,
        nullable=True,
    )

    checkout_id: str | None = Field(
        default=None,
        max_length=100,
        nullable=True,
        unique=True,
        index=True,
    )

    payment_link: str | None = Field(
        default=None,
        max_length=500,
        nullable=True,
    )

    expires_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
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