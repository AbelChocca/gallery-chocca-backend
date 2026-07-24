from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.inventory.types.inventory import AvailabilityStatus
from app.features.inventory.types.inventory_location import InventoryLocationType


@dataclass
class InventoryLocationStockDTO:
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