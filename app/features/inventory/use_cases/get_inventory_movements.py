from app.features.inventory.services.inventory_movement_service import InventoryMovementService
from app.features.inventory.dtos.inventory_movements import (
    InventoryMovementFilters,
    InventoryMovementAdminPaginatedDTO,
    InventoryMovementAdminDTO,
)


class GetInventoryMovementsUseCase:
    def __init__(
        self,
        inventory_service: InventoryMovementService,
    ):
        self._inventory_service = inventory_service

    async def execute(
        self,
        *,
        filters: InventoryMovementFilters,
        page: int = 1,
        limit: int = 20
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