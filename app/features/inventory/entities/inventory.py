from app.features.inventory.types.inventory import AvailabilityStatus
from app.features.inventory.types.inventory_movement import InventoryOwnerType

from datetime import datetime
from decimal import Decimal


class Inventory:

    def __init__(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        location_id: int,
        quantity: Decimal = Decimal("0"),
        reserved_quantity: Decimal = Decimal("0"),
        minimum_stock: Decimal = Decimal("0"),
        last_movement_at: datetime | None = None,
        id: int | None = None,
    ) -> None:

        self.id = id

        self.owner_type = owner_type
        self.owner_id = owner_id

        self.location_id = location_id

        self.quantity = quantity
        self.reserved_quantity = reserved_quantity
        self.minimum_stock = minimum_stock

        self.last_movement_at = last_movement_at

    @property
    def available_quantity(self) -> Decimal:
        return self.quantity - self.reserved_quantity

    @property
    def availability_status(
        self,
    ) -> AvailabilityStatus:

        if self.available_quantity <= Decimal("0"):
            return AvailabilityStatus.OUT_OF_STOCK

        if self.available_quantity <= self.minimum_stock:
            return AvailabilityStatus.CRITICAL

        return AvailabilityStatus.AVAILABLE