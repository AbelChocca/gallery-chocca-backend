from app.features.inventory.services.inventory_movement_service import InventoryMovementService
from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service
from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_location_service import InventoryLocationService

from fastapi import Depends

def get_inventory_movement_service(
        uow: UnitOfWork = Depends(get_uow),
        pagination_service: PaginationService = Depends(get_pagination_service)
        ) -> InventoryMovementService:
    return InventoryMovementService(
        inventory_movement_repo=uow.inventory_movements,
        pagination_service=pagination_service
    )

def get_inventory_location_service(
    uow: UnitOfWork = Depends(get_uow),
) -> InventoryLocationService:
    return InventoryLocationService(inventory_location_repository=uow.inventory_locations)

def get_inventory_service(
        uow: UnitOfWork = Depends(get_uow)
) -> InventoryService:
    return InventoryService(
        inventory_repository=uow.inventory
    )