
from app.features.inventory.services.inventory_service import (
    InventoryService,
)
from app.features.inventory.types.inventory_movement import (
    InventoryOwnerType,
)
from app.features.inventory.dtos.inventory import (
    UpdateInventoryLocationDTO,
)

from app.features.locations.services.location_service import (
    LocationService,
)
from app.features.locations.types import LocationType

from app.core.exceptions import (
    ValidationError,
    InvalidOperation,
)


INVENTORY_LOCATION_TYPES = frozenset({
    LocationType.STORE,
    LocationType.WORKSHOP,
    LocationType.WAREHOUSE,
})


class UpdateInventoryLocationsUseCase:

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
        owner_id: int,
        owner_type: InventoryOwnerType,
        locations: list[UpdateInventoryLocationDTO],
    ) -> None:

        if not locations:
            raise ValidationError(
                "Se requiere al menos una ubicación de inventario."
            )

        location_ids = [
            location.location_id
            for location in locations
        ]

        if len(location_ids) != len(set(location_ids)):
            raise ValidationError(
                "No se permiten ubicaciones repetidas."
            )

        # Validar ubicaciones solicitadas
        for dto in locations:
            location = await self._location_service.get_by_id(
                location_id=dto.location_id,
            )

            if location is None:
                raise ValidationError(
                    f"La ubicación {dto.location_id} no existe."
                )

            if not location.is_active:
                raise InvalidOperation(
                    f"La ubicación '{location.name}' está inactiva."
                )

            if location.type not in INVENTORY_LOCATION_TYPES:
                raise InvalidOperation(
                    f"La ubicación '{location.name}' "
                    "no admite inventario."
                )

        current_inventories = (
            await self._inventory_service.get_owner_inventories(
                owner_id=owner_id,
                owner_type=owner_type,
            )
        )

        current_by_location = {
            inventory.location_id: inventory
            for inventory in current_inventories
        }

        incoming_by_location = {
            dto.location_id: dto
            for dto in locations
        }

        current_ids = set(current_by_location)
        incoming_ids = set(incoming_by_location)

        # Actualizar existentes
        for location_id in current_ids & incoming_ids:
            inventory = current_by_location[location_id]
            dto = incoming_by_location[location_id]

            await self._inventory_service.update_inventory(
                inventory_id=inventory.id,
                minimum_stock=dto.minimum_stock,
                unit_price=dto.unit_price,
            )

        # Crear nuevos
        for location_id in incoming_ids - current_ids:
            dto = incoming_by_location[location_id]

            await self._inventory_service.create_inventory(
                owner_id=owner_id,
                owner_type=owner_type,
                location_id=location_id,
                unit_price=dto.unit_price,
                minimum_stock=dto.minimum_stock,
            )

        # Eliminar ubicaciones retiradas
        for location_id in current_ids - incoming_ids:
            inventory = current_by_location[location_id]

            await self._inventory_service.delete_inventory(
                inventory_id=inventory.id,
            )
