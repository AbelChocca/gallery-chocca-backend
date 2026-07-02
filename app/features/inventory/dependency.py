from app.features.inventory.inventory_service import InventoryService
from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service
from app.features.inventory.types import InventoryOwnerType
from app.features.inventory.resolvers.base import InventoryOwnerResolver

from app.features.inventory.use_cases.create_movement import (
    CreateMovementUseCase
)

from app.features.inventory.use_cases.create_bulk_movement import (
    CreateBulkMovementUseCase
)

from app.features.inventory.use_cases.get_inventory_movements import (
    GetInventoryMovementsUseCase
)

from app.features.inventory.resolvers.dependency import get_inventory_owner_resolvers
from app.infra.cache.redis_service import RedisService
from app.infra.cache.dependency import get_cache_service

from fastapi import Depends

def get_inventory_service(
        uow: UnitOfWork = Depends(get_uow),
        pagination_service: PaginationService = Depends(get_pagination_service)
        ) -> InventoryService:
    return InventoryService(
        inventory_movement_repo=uow.inventory,
        pagination_service=pagination_service
    )

def get_create_movement_use_case(
    owner_resolvers: dict[
        InventoryOwnerType,
        InventoryOwnerResolver
    ] = Depends(
        get_inventory_owner_resolvers
    ),
    inventory_service: InventoryService = Depends(get_inventory_service),
    cache_service: RedisService = Depends(get_cache_service),
) -> CreateMovementUseCase:
    return CreateMovementUseCase(
        owner_resolvers=owner_resolvers,
        inventory_service=inventory_service,
        cache_service=cache_service
    )

def get_create_bulk_movement_use_case(
    owner_resolvers: dict[
        InventoryOwnerType,
        InventoryOwnerResolver
    ] = Depends(
        get_inventory_owner_resolvers
    ),
    inventory_service: InventoryService = Depends(get_inventory_service),
    cache_service: RedisService = Depends(get_cache_service),
) -> CreateBulkMovementUseCase:
    return CreateBulkMovementUseCase(
        owner_resolvers=owner_resolvers,
        inventory_service=inventory_service,
        cache_service=cache_service
    )

def get_inventory_movements_use_case(
    inventory_service: InventoryService = Depends(get_inventory_service),
    cache_service: RedisService = Depends(get_cache_service),
) -> GetInventoryMovementsUseCase:
    return GetInventoryMovementsUseCase(
        inventory_service=inventory_service,
        cache_service=cache_service
    )