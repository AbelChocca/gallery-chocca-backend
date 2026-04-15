from sqlmodel import SQLModel, Field, Enum, Column, DateTime
from app.domain.inventory.data_models import InventoryMovementType
from datetime import datetime, timezone

class InventoryMovementTable(SQLModel):
    __name__ = "inventory_movement"
    id: int | None = Field(default=None, primary_key=True)
    variant_size_id: int = Field(ge=1)
    type: InventoryMovementType = Field(
        sa_column=(
            Column(Enum(InventoryMovementType, name="inventory_movement_type"), nullable=False)
        )
    )
    quantity: int
    previous_stock: int 
    new_stock: int 
    reason: str | None = Field(default=None, nullable=True, max_length=255)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )