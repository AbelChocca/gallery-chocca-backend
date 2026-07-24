from app.features.inventory.services.inventory_movement_service import InventoryMovementService
from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.dtos.inventory_movements import CreateMovementCommand
from app.features.inventory.types.inventory_reference import InventoryReferenceType

class CreateMovementUseCase:
    def __init__(
        self,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
    ):
        self._inventory_service = inventory_service
        self._inventory_movement_service = inventory_movement_service

    async def execute(
        self,
        command: CreateMovementCommand
    ) -> dict:

        result = await self._inventory_service.update_stock(
            owner_type=command.owner_type,
            owner_id=command.owner_id,
            location_id=command.location_id,
            quantity=command.quantity,
            movement_type=command.type,
        )

        if result is None:
            result = await self._inventory_service.create_inventory_with_stock(
                owner_type=command.owner_type,
                owner_id=command.owner_id,
                location_id=command.location_id,
                quantity=command.quantity,
            )


        await self._inventory_movement_service.create_movement(
            owner_type=command.owner_type,
            owner_id=result.owner_id,
            owner_name=command.owner_name,
            owner_code=command.owner_code,
            location_id=command.location_id,
            movement_type=command.type,
            quantity=command.quantity, 
            prev_stock=result.previous_stock,
            new_stock=result.current_stock,
            performed_by=command.performed_by,
            reason=command.reason,
            reference_type=InventoryReferenceType.MANUAL_ADJUSTMENT
        )

        return {
            "message": "Entity stock updated successfully."
        }