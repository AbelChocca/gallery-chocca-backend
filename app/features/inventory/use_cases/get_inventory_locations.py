from app.features.inventory.services.inventory_service import (
    InventoryService,
)
from app.features.locations.services.location_service import (
    LocationService,
)
from app.features.locations.entities.location import Location
from app.features.inventory.types.inventory_movement import (
    InventoryOwnerType,
)


class GetInventoryLocationsUseCase:

    def __init__(
        self,
        inventory_service: InventoryService,
        location_service: LocationService,
    ) -> None:
        self._inventory_service = inventory_service
        self._location_service = location_service

    async def execute(
        self,
        *,
        search: str | None = None,
        is_active: bool | None = None,
        owner_type: InventoryOwnerType | None = None,
        owner_id: int | None = None,
    ) -> list[Location]:

        location_ids: list[int] | None = None

        if owner_type is not None and owner_id is not None:
            location_ids = (
                await self._inventory_service.get_location_ids_by_owner(
                    owner_type=owner_type,
                    owner_id=owner_id,
                )
            )

            if not location_ids:
                return []

        return await self._location_service.get_inventory_locations(
            search=search,
            is_active=is_active,
            location_ids=location_ids,
        )