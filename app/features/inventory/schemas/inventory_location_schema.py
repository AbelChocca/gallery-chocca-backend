from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

from app.features.locations.types import LocationType
from app.features.inventory.types.inventory import AvailabilityStatus

class InventoryLocationStockSchema(BaseModel):
    inventory_id: int

    location_id: int
    location_name: str
    location_type: LocationType

    quantity: Decimal
    reserved_quantity: Decimal
    available_quantity: Decimal

    minimum_stock: Decimal

    address: str | None

    availability_status: AvailabilityStatus

    last_movement_at: datetime | None = None

    valuation: Decimal

    unit_price: Decimal | None = None

    model_config = ConfigDict(from_attributes=True)

class InventoryLocationResponseSchema(BaseModel):
    id: int

    name: str

    type: LocationType

    address: str | None

    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class InventoryLocationFiltersSchema(BaseModel):
    search: str | None = None

    is_active: bool | None = None

    location_type: LocationType | None = None

