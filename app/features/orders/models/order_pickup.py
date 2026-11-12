
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, DateTime, Numeric
from sqlmodel import Field, SQLModel


class OrderPickupTable(SQLModel, table=True):
    __tablename__ = "order_pickups"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    order_id: int = Field(
        foreign_key="orders.id",
        nullable=False,
        unique=True,
        index=True,
    )

    location_id: int = Field(
        foreign_key="locations.id",
        nullable=False,
        index=True,
    )

    # Snapshot de la tienda al crear el pedido
    location_name: str = Field(
        max_length=150,
        nullable=False,
    )

    location_address: str = Field(
        max_length=255,
        nullable=False,
    )

    location_ubigeo_code: str = Field(
        max_length=6,
        nullable=False,
    )

    location_latitude: Decimal | None = Field(
        default=None,
        sa_type=Numeric(9, 6),
    )

    location_longitude: Decimal | None = Field(
        default=None,
        sa_type=Numeric(9, 6),
    )

    location_phone: str | None = Field(
        default=None,
        max_length=30,
    )

    location_reference: str | None = Field(
        default=None,
        max_length=255,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
