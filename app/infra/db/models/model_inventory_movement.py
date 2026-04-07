from sqlmodel import SQLModel, Field, Enum, Column, DateTime
from app.infra.db.types import InventoryMovementType
from datetime import datetime, timezone


class InventoryMovement(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    variant_id: int = Field(ge=1)
    type: InventoryMovementType = Field(
        sa_column=(
            Column(Enum(InventoryMovementType, name="inventory_movement_type"))
        ), 
        nullable=False
        )
    quantity: int = Field(gt=0)
    previous_stock: int 
    new_stock: int 
    reason: str | None = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )