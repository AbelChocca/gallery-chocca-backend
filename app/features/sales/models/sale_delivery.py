from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, SQLModel

from app.features.sales.types.sale_delivery import DeliveryStatus, CourierProvider


class SaleDelivery(SQLModel, table=True):
    __tablename__ = "sale_delivery"

    sale_id: int = Field(
        foreign_key="sale.id",
        primary_key=True,
    )

    status: DeliveryStatus = Field(
        default=DeliveryStatus.PENDING,
        sa_column=Column(
            ENUM(
                DeliveryStatus,
                name="delivery_status",
                create_type=False,
            ),
            nullable=False,
        ),
    )

    recipient_name: str = Field(
        max_length=150,
        nullable=False,
    )

    recipient_phone: str = Field(
        max_length=20,
        nullable=False,
    )

    address: str = Field(
        max_length=255,
        nullable=False,
    )

    department: str = Field(
        max_length=100,
        nullable=False,
    )

    province: str = Field(
        max_length=100,
        nullable=False,
    )

    district: str = Field(
        max_length=100,
        nullable=False,
    )

    reference: str | None = Field(
        default=None,
        max_length=255,
    )

    shipping_cost: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
        ),
    )

    courier: CourierProvider | None = Field(
        default=None,
        sa_column=Column(
            ENUM(
                CourierProvider,
                name="courier_provider",
                create_type=False,
            ),
            nullable=True,
        ),
    )

    tracking_code: str | None = Field(
        default=None,
        max_length=100,
    )

    shipped_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    estimated_delivery_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    delivered_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
        default_factory=lambda: datetime.now(timezone.utc),
    )