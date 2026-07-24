from app.features.inventory.types.inventory_location import InventoryLocationType

from datetime import datetime


class InventoryLocation:

    def __init__(
        self,
        *,
        name: str,
        type: InventoryLocationType,
        address: str | None = None,
        is_active: bool = True,
        created_at: datetime | None = None,
        id: int | None = None,
    ) -> None:
        self.id = id

        self.name = name
        self.type = type

        self.address = address
        self.is_active = is_active

        self.created_at = created_at