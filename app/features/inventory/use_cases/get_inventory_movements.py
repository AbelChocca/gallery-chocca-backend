from app.features.inventory.inventory_service import InventoryService
from app.features.inventory.dto import (
    InventoryMovementFilters,
    InventoryMovementAdminPaginatedDTO,
    InventoryMovementAdminDTO,
)
from app.infra.cache.redis_service import RedisService

from app.features.inventory.constants import INVENTORY_MOVEMENTS_CACHE_KEY_TAG

class GetInventoryMovementsUseCase:
    def __init__(
        self,
        inventory_service: InventoryService,
        cache_service: RedisService,
    ):
        self._inventory_service = inventory_service
        self._cache_service = cache_service

    async def execute(
        self,
        *,
        filters: InventoryMovementFilters,
        page: int = 1,
        limit: int = 20
    ) -> InventoryMovementAdminPaginatedDTO:

        return await self._cache_service.get_or_set_with_lock_v2(
            tag=INVENTORY_MOVEMENTS_CACHE_KEY_TAG,
            callback=self._get_admin_movements,
            kwargs={
                "filters": filters,
                "page": page,
                "limit": limit
            },
            key_args={
                "page": page,
                "limit": limit,
                "filters": filters.to_dict() if filters else {}
            },
            serializer=lambda dto: dto.to_dict(),
            deserializer=InventoryMovementAdminPaginatedDTO.from_dict
        )
    
    async def _get_admin_movements(
        self,
        *,
        filters: InventoryMovementFilters,
        page: int,
        limit: int
    ) -> InventoryMovementAdminPaginatedDTO:

        movements = (
            await self._inventory_service
            .get_paginated_inventory_movements(
                filter_command=filters,
                page=page,
                limit=limit
            )
        )

        return InventoryMovementAdminPaginatedDTO(
            items=[
                InventoryMovementAdminDTO(
                    id=movement.id,

                    owner_id=movement.owner_id,
                    owner_type=movement.owner_type,

                    owner_code=movement.owner_code,
                    owner_name=movement.owner_name,

                    type=movement.type,

                    quantity=movement.quantity,

                    previous_stock=movement.previous_stock,
                    new_stock=movement.new_stock,

                    reason=movement.reason,
                    created_at=movement.created_at
                )
                for movement in movements.items
            ],
            pagination=movements.pagination,
            total_items=movements.total_items
        )