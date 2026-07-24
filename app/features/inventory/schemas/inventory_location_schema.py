from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

from app.features.inventory.types.inventory_location import (
    InventoryLocationType,
)
from app.features.inventory.types.inventory import AvailabilityStatus

class InventoryLocationStockSchema(BaseModel):
    inventory_id: int

    location_id: int
    location_name: str
    location_type: InventoryLocationType

    quantity: Decimal
    reserved_quantity: Decimal
    available_quantity: Decimal

    minimum_stock: Decimal

    address: str | None

    availability_status: AvailabilityStatus

    last_movement_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class InventoryLocationResponseSchema(BaseModel):
    id: int

    name: str

    type: InventoryLocationType

    address: str | None

    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class InventoryLocationFiltersSchema(BaseModel):
    search: str | None = None

    is_active: bool | None = None

    location_type: InventoryLocationType | None = None

class CreateInventoryLocationSchema(BaseModel):
    name: str = Field(max_length=100)

    type: InventoryLocationType

    address: str | None = Field(
        default=None,
        max_length=255,
    )

class UpdateInventoryLocationSchema(BaseModel):
    name: str = Field(max_length=100)

    type: InventoryLocationType

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    is_active: bool


class ToggleInventoryLocationSchema(BaseModel):
    is_active: bool