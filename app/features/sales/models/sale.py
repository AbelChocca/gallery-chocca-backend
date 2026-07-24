from app.features.sales.types.sale import SaleChannel, SaleStatus

from datetime import datetime, timezone
from decimal import Decimal

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Numeric, DateTime
from sqlalchemy.dialects.postgresql import ENUM


class Sale(SQLModel, table=True):
    __tablename__ = "sale"

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    customer_id: int | None = Field(
        default=None,
        foreign_key="customer.id"
    )

    seller_id: int | None = Field(
        default=None,
        foreign_key="usertable.id",
    )

    location_id: int = Field(
        foreign_key="inventory_location.id",
        nullable=False
    )

    channel: SaleChannel = Field(
        sa_column=Column(
            ENUM(
                SaleChannel,
                name="sale_channel",
                create_type=False
            ),
            nullable=False
        )
    )

    status: SaleStatus = Field(
        default=SaleStatus.PENDING,
        sa_column=Column(
            ENUM(
                SaleStatus,
                name="sale_status",
                create_type=False
            ),
            nullable=False
        )
    )

    subtotal: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

    discount: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

    tax: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

    total: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

    code: str | None = Field(
        default=None,
        max_length=25
    )

    notes: str | None = Field(
        default=None,
        max_length=255
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )