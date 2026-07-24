from app.features.inventory.services.inventory_movement_service import InventoryMovementService

from app.features.inventory.use_cases.create_movement import (
    CreateMovementUseCase
)

from app.features.inventory.use_cases.create_bulk_movement import (
    CreateBulkMovementUseCase
)

from app.features.inventory.use_cases.get_inventory_movements import (
    GetInventoryMovementsUseCase
)

from app.features.inventory.services.inventory_service import (
    InventoryService,
)

from app.features.inventory.dependencies.services import get_inventory_movement_service, get_inventory_service

from fastapi import Depends

def get_create_movement_use_case(
    inventory_service: InventoryService = Depends(get_inventory_service),
    inventory_movement_service: InventoryMovementService = Depends(get_inventory_movement_service)
) -> CreateMovementUseCase:
    return CreateMovementUseCase(
        inventory_service=inventory_service,
        inventory_movement_service=inventory_movement_service
    )

def get_create_bulk_movement_use_case(
    inventory_movement_service: InventoryMovementService = Depends(get_inventory_movement_service),
    inventory_service: InventoryService = Depends(get_inventory_service),
) -> CreateBulkMovementUseCase:
    return CreateBulkMovementUseCase(
        inventory_service=inventory_service,
        inventory_movement_service=inventory_movement_service
    )

def get_inventory_movements_use_case(
    inventory_service: InventoryMovementService = Depends(get_inventory_movement_service),
) -> GetInventoryMovementsUseCase:
    return GetInventoryMovementsUseCase(
        inventory_service=inventory_service,
    )