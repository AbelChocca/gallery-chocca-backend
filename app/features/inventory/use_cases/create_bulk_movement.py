from app.features.inventory.services.inventory_movement_service import InventoryMovementService

from app.features.inventory.dtos.inventory_movements import (
    CreateBulkMovementCommand
)

from app.features.inventory.types.inventory_reference import InventoryReferenceType
from app.features.inventory.services.inventory_service import InventoryService


class CreateBulkMovementUseCase:
    def __init__(
        self,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
    ):
        self._inventory_service = inventory_service
        self._inventory_movement_service = inventory_movement_service

    async def execute(
        self,
        command: CreateBulkMovementCommand,
        user_id: int
    ) -> dict:
         
        stock_results = await self._inventory_service.update_stock_many(
            owner_type=command.owner_type,
            movement_type=command.type,
            movement_items=command.items,
        )

        results_by_owner = {
            result.owner_id: result
            for result in stock_results
        }

        for item in command.items:

            stock_result = results_by_owner[item.owner_id]

            await self._inventory_movement_service.create_movement(
                owner_type=command.owner_type,
                owner_id=item.owner_id,
                owner_code=item.owner_code,
                location_id=command.location_id,
                owner_name=item.owner_name,
                movement_type=command.type,
                quantity=item.quantity,
                prev_stock=stock_result.previous_stock,
                new_stock=stock_result.current_stock,
                reference_type=InventoryReferenceType.MANUAL_ADJUSTMENT,
                performed_by=user_id,
                reason=command.reason
            )

        return {
            "message": (
                "Inventories updated successfully."
            )
        }