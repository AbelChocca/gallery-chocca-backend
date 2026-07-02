from sqlmodel import SQLModel, Field, String, Index
from app.features.inventory.types import InventoryMovementType, InventoryOwnerType
from datetime import datetime, timezone
from sqlalchemy import Enum, Column, DateTime


class InventoryMovementTable(SQLModel, table=True):
    __tablename__ = "inventory_movement"
    __table_args__ = (
        Index(
            "ix_inventory_movement_owner",
            "owner_type",
            "owner_id"
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
    owner_id: int = Field(nullable=False)

    owner_code: str = Field(
        sa_column=Column(
            String(100),
            nullable=False,
            index=True
        )
    )

    owner_name: str = Field(
        sa_column=Column(
            String(255),
            nullable=False,
            index=True
        )
    )

    type: InventoryMovementType = Field(
        sa_column=Column(
            Enum(
                InventoryMovementType,
                name="inventory_movement_type"
            ),
            nullable=False
        )
    )

    quantity: int

    previous_stock: int

    new_stock: int

    reason: str | None = Field(
        default=None,
        max_length=255
    )   

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True)
        )
    )