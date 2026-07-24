from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    Enum
)
from sqlmodel import Field, SQLModel

from app.features.inventory.types.inventory_movement import InventoryOwnerType


class InventoryTable(SQLModel, table=True):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint(
            "owner_type",
            "owner_id", 
            "location_id",
            name="uq_inventory_owner_location",
        ),
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_quantity_positive",
        ),
        CheckConstraint(
            "reserved_quantity >= 0",
            name="ck_inventory_reserved_positive",
        ),
        CheckConstraint(
            "reserved_quantity <= quantity",
            name="ck_inventory_reserved_not_greater",
        ),
        CheckConstraint(
            "minimum_stock >= 0",
            name="ck_inventory_minimum_stock_positive",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    owner_type: InventoryOwnerType = Field(
        sa_column=Column(
            Enum(
                InventoryOwnerType,
                name="inventory_owner_type"
            ),
            nullable=False
        )
    )

    owner_id: int = Field(
        nullable=False
    )

    location_id: int = Field(
        sa_column=Column(
            ForeignKey("inventory_location.id"),
            nullable=False,
        )
    )

    quantity: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
            default=Decimal("0"),
        )
    )

    reserved_quantity: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
            default=Decimal("0"),
        )
    )

    minimum_stock: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
            default=Decimal("0"),
        )
    )

    last_movement_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True)
        ),
    )