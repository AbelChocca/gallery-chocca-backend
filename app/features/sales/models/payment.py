from app.features.sales.types.payment import PaymentMethod, PaymentStatus

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import CheckConstraint, Column, Numeric, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, SQLModel

class Payment(SQLModel, table=True):
    __tablename__ = "payment"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_payment_amount_positive",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    sale_id: int = Field(
        foreign_key="sale.id",
        nullable=False,
    )

    method: PaymentMethod = Field(
        sa_column=Column(
            ENUM(
                PaymentMethod,
                name="payment_method",
                create_type=False,
            ),
            nullable=False,
        )
    )

    status: PaymentStatus = Field(
        default=PaymentStatus.PENDING,
        sa_column=Column(
            ENUM(
                PaymentStatus,
                name="payment_status",
                create_type=False,
            ),
            nullable=False,
        )
    )

    amount: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )