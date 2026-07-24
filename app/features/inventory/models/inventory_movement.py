from sqlmodel import SQLModel, Field, String, Index
from app.features.inventory.types.inventory_movement import InventoryMovementType, InventoryOwnerType
from app.features.inventory.types.inventory_reference import InventoryReferenceType
from datetime import datetime, timezone
from sqlalchemy import Enum, Column, DateTime, Numeric, CheckConstraint
from decimal import Decimal

class InventoryMovementTable(SQLModel, table=True):
    __tablename__ = "inventory_movement"
    __table_args__ = (
        CheckConstraint("quantity <> 0", name="ck_inventory_movement_quantity_non_zero"),
        CheckConstraint(
            "previous_stock >= 0",
            name="ck_inventory_movement_previous_positive",
        ),
        CheckConstraint(
            "new_stock >= 0",
            name="ck_inventory_movement_new_positive",
        ),
        Index(
            "ix_inventory_movement_owner",
            "owner_type",
            "owner_id"
        ),
        Index("ix_inventory_movement_location", "location_id"),
        Index("ix_inventory_movement_created_at", "created_at"),
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

    location_id: int = Field(foreign_key="inventory_location.id", nullable=True)

    type: InventoryMovementType = Field(
        sa_column=Column(
            Enum(
                InventoryMovementType,
                name="inventory_movement_type"
            ),
            nullable=False
        )
    )

    reference_type: InventoryReferenceType | None = Field(
    default=None,
    sa_column=Column(
        Enum(
            InventoryReferenceType,
            name="inventory_reference_type",
        ),
        nullable=True,
    ),
)

    reference_id: int | None = None

    performed_by: int | None = Field(
        default=None,
        foreign_key="usertable.id",
    )

    quantity: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

    previous_stock: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

    new_stock: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

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