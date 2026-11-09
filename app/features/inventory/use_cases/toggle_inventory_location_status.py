
from app.features.inventory.services.inventory_service import (
    InventoryService,
)

from app.features.locations.services.location_service import (
    LocationService,
)
from app.core.exceptions import ValidationError


class ToggleInventoryLocationStatusUseCase:

    def __init__(
        self,
        location_service: LocationService,
        inventory_service: InventoryService,
    ) -> None:
        self._location_service = location_service
        self._inventory_service = inventory_service

    async def execute(
        self,
        *,
        location_id: int,
        is_active: bool,
    ) -> None:

        location = await self._location_service.get_by_id(
            location_id=location_id,
        )

        if location is None:
            raise ValidationError(
                "La ubicación seleccionada no existe."
            )

        if not is_active:
            await (
                self._inventory_service
                .validate_location_has_no_stock(
                    location_id=location_id,
                )
            )

        await self._location_service.set_active_status(
            location_id=location_id,
            is_active=is_active,
        )
