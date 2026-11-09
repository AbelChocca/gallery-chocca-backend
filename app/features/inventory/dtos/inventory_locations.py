from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.inventory.types.inventory import AvailabilityStatus
from app.features.locations.types import LocationType

@dataclass
class InventoryLocationStockDTO:
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

    valuation: Decimal

    unit_price: Decimal | None = None
    last_movement_at: datetime | None = None