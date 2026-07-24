from app.features.inventory.services.inventory_location_service import InventoryLocationService
from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.types.inventory_movement import InventoryOwnerType

from app.features.inventory.dtos.inventory import UpdateInventoryLocationDTO

from app.core.exceptions import ValidationError, InvalidOperation

class UpdateInventoryLocationsUseCase:

    def __init__(
        self,
        inventory_service: InventoryService,
        inventory_location_service: InventoryLocationService,
    ) -> None:
        self._inventory_service = inventory_service
        self._inventory_location_service = inventory_location_service


    async def execute(
        self,
        *,
        owner_id: int,
        owner_type: InventoryOwnerType,
        locations: list[UpdateInventoryLocationDTO],
    ) -> None:

        if not locations:
            raise ValidationError(
                "Se requiere al menos una ubicacion de inventario."
            )


        location_ids = [
            location.location_id
            for location in locations
        ]

        if len(location_ids) != len(set(location_ids)):
            raise ValidationError(
                "No se permiten ubicaciones repetidas."
            )


        for location in locations:

            inventory_location = (
                await self._inventory_location_service.get_location_by_id(
                    location.location_id
                )
            )

            if not inventory_location.is_active:
                raise InvalidOperation(
                    f"Inventory location '{inventory_location.name}' is inactive."
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


        # actualizar existentes
        for location_id in (
            current_by_location.keys()
            & incoming_by_location.keys()
        ):

            inventory = current_by_location[location_id]
            dto = incoming_by_location[location_id]

            await self._inventory_service.update_minimum_stock(
                inventory_id=inventory.id,
                minimum_stock=dto.minimum_stock,
            )


        # crear nuevos
        for location_id in (
            incoming_by_location.keys()
            - current_by_location.keys()
        ):

            dto = incoming_by_location[location_id]

            await self._inventory_service.create_inventory(
                owner_id=owner_id,
                owner_type=owner_type,
                location_id=location_id,
                minimum_stock=dto.minimum_stock,
            )


        # eliminar removidos
        for location_id in (
            current_by_location.keys()
            - incoming_by_location.keys()
        ):

            inventory = current_by_location[location_id]

            await self._inventory_service.delete_inventory(
                inventory_id=inventory.id,
            )