from decimal import Decimal

from sqlalchemy import Numeric
from sqlmodel import Field, SQLModel


class OrderAddressTable(SQLModel, table=True):
    __tablename__ = "order_addresses"

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

    recipient_name: str = Field(
        max_length=150,
        nullable=False,
    )

    phone: str = Field(
        max_length=20,
        nullable=False,
    )

    ubigeo_code: str = Field(
        foreign_key="ubigeos.code",
        nullable=False,
        max_length=6,
        index=True,
    )

    address: str = Field(
        max_length=255,
        nullable=False,
    )

    latitude: Decimal = Field(
        sa_type=Numeric(9, 6),
        nullable=False,
    )

    longitude: Decimal = Field(
        sa_type=Numeric(9, 6),
        nullable=False,
    )

    reference: str | None = Field(
        default=None,
        max_length=255,
    )

    delivery_instructions: str | None = Field(
        default=None,
        max_length=500,
    )