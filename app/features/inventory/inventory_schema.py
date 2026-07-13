from pydantic import BaseModel, Field, ConfigDict
from app.features.inventory.dto import InventoryMovementType, InventoryOwnerType
from app.shared.pagination.schema import PaginatedResponseSchema
from datetime import datetime, date
from decimal import Decimal

class MovementItemSchema(BaseModel):
    owner_id: int = Field(gt=0)
    quantity: Decimal

class CreateMovementSchema(BaseModel):
    owner_id: int
    owner_type: InventoryOwnerType
    type: InventoryMovementType
    quantity: Decimal
    reason: str | None = Field(
        default=None,
        max_length=255
    )

class CreateBulkMovementSchema(BaseModel):
    owner_type: InventoryOwnerType
    type: InventoryMovementType
    reason: str | None = None
    items: list[MovementItemSchema]

class InventoryMovementRead(BaseModel):
    id: int

    owner_id: int
    owner_type: InventoryOwnerType

    owner_code: str
    owner_name: str

    type: InventoryMovementType

    quantity: Decimal
    previous_stock: Decimal
    new_stock: Decimal

    created_at: datetime
    reason: str | None = None

    model_config = ConfigDict(from_attributes=True)

class InventoryMovementFilterSchema(BaseModel):
    from_date: date | None = None
    to_date: date | None = None

    search: str | None = None
    owner_type: InventoryOwnerType | None = None
    owner_id: int | None = None

    type: InventoryMovementType | None = None

class GetInventoryMovementsResponse(
    PaginatedResponseSchema[InventoryMovementRead]
):
    pass