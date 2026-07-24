from app.features.inventory.services.inventory_location_service import (
    InventoryLocationService,
)
from app.features.inventory.services.inventory_service import (
    InventoryService,
)


class ToggleInventoryLocationStatusUseCase:

    def __init__(
        self,
        inventory_location_service: InventoryLocationService,
        inventory_service: InventoryService,
    ) -> None:
        self._inventory_location_service = inventory_location_service
        self._inventory_service = inventory_service

    async def execute(
        self,
        *,
        location_id: int,
        is_active: bool,
    ) -> None:

        if not is_active:
            await (
                self._inventory_service.validate_location_has_no_stock(
                    location_id=location_id,
                )
            )

        await self._inventory_location_service.toggle_status(
            location_id=location_id,
            is_active=is_active,
        )