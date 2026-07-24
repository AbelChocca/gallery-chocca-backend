from app.core.exceptions import (
    ValidationError,
    ValueNotFound,
    InvalidOperation
)
from app.features.inventory.entities.inventory_location import InventoryLocation
from app.features.inventory.repositories.inventory_location_repository import (
    InventoryLocationRepository,
)
from app.features.inventory.types.inventory_location import InventoryLocationType


class InventoryLocationService:

    def __init__(
        self,
        inventory_location_repository: InventoryLocationRepository,
    ) -> None:
        self._repository = inventory_location_repository

    async def get_locations(
        self,
        *,
        search: str | None = None,
        is_active: bool | None = None,
        location_type: InventoryLocationType | None = None,
    ) -> list[InventoryLocation]:

        return await self._repository.get_locations(
            search=search.strip() if search else None,
            is_active=is_active,
            location_type=location_type,
        )

    async def create_location(
        self,
        *,
        name: str,
        type: InventoryLocationType,
        address: str | None,
    ) -> InventoryLocation:

        name = name.strip()

        if not name:
            raise ValidationError(
                "The location name is required."
            )

        existing = await self._repository.get_by_name(name)

        if existing:
            raise ValidationError(
                "A location with this name already exists."
            )

        location = InventoryLocation(
            name=name,
            type=type,
            address=address.strip() if address else None,
        )

        return await self._repository.save(location)
    
    async def get_location_by_id(
            self,
            location_id: int
    ) -> InventoryLocation:
        return await self._repository.get_by_id(location_id)

    async def update_location(
        self,
        *,
        location_id: int,
        name: str,
        type: InventoryLocationType,
        address: str | None,
        is_active: bool,
    ) -> InventoryLocation:

        location = await self._repository.get_by_id(location_id)

        if location is None:
            raise ValueNotFound(
                "Inventory location not found."
            )

        name = name.strip()

        if not name:
            raise ValidationError(
                "The location name is required."
            )

        existing = (
            await self._repository.get_by_name_except_id(
                name=name,
                location_id=location_id,
            )
        )

        if existing:
            raise ValidationError(
                "A location with this name already exists."
            )

        location.name = name
        location.type = type
        location.address = (
            address.strip()
            if address
            else None
        )
        location.is_active = is_active

        return await self._repository.save(location)
    
    async def toggle_status(
        self,
        *,
        location_id: int,
        is_active: bool,
    ) -> None:

        location = await self._repository.get_by_id(
            location_id
        )

        if location is None:
            raise ValueNotFound(
                "Inventory location not found."
            )

        if location.is_active == is_active:
            raise InvalidOperation(
                (
                    "Inventory location is already active."
                    if is_active
                    else "Inventory location is already inactive."
                )
            )

        await self._repository.toggle_status(
            location_id=location_id,
            is_active=is_active,
        )