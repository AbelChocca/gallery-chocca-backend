from app.features.inventory.dto import InventoryMovementFilters, InventoryMovementDTO, InventoryMovementPaginatedDTO
from app.infra.db.repositories.sqlalchemy_inventory_movement_repo import PostgresInventoryMovementReposity
from app.features.inventory.inventory_movement_entity import InventoryMovement
from app.shared.pagination.pagination_service import PaginationService
from app.features.inventory.types import InventoryMovementType, InventoryOwnerType
from decimal import Decimal

class InventoryService:
    def __init__(
            self,
            inventory_movement_repo: PostgresInventoryMovementReposity,
            pagination_service: PaginationService,
        ):
        self._inventory_movement_repo = inventory_movement_repo
        self._pagination_service = pagination_service

    async def create_movement(
        self,
        *,
        movement_type: InventoryMovementType,
        owner_type: InventoryOwnerType,
        owner_id: int,
        owner_name: str,
        owner_code: str,
        quantity: Decimal,
        prev_stock: Decimal,
        new_stock: Decimal,
        reason: str,
    ) -> None:
        new_movement = InventoryMovement.create(
            owner_type=owner_type,
            owner_id=owner_id,
            owner_code=owner_code,
            owner_name=owner_name,
            movement_type=movement_type,
            quantity=quantity,
            previous_stock=prev_stock,
            new_stock=new_stock,
            reason=reason
        )

        await self._inventory_movement_repo.save(new_movement)
        
    async def get_paginated_inventory_movements(
        self,
        filter_command: InventoryMovementFilters,
        page: int,
        limit: int
    ) -> InventoryMovementPaginatedDTO:
        offset = self._pagination_service.get_offset(page, limit)
        movements = await self.get_inventory_movements(filter_command, offset, limit)

        total_movements = await self._inventory_movement_repo.count_with_filters(filter_command)

        items = [
            InventoryMovementDTO.from_entity(movement)
            for movement in movements
        ]

        return InventoryMovementPaginatedDTO.create(
            items=items,
            total_items=total_movements,
            current_page=self._pagination_service.get_current_page(
                offset,
                limit
            ),
            total_pages=self._pagination_service.get_total_pages(
                total_movements,
                limit
            )
        )
    
    async def get_movement_by_id(
        self,
        movement_id: int
    ) -> InventoryMovement | None:
        return await self._inventory_movement_repo.get_by_id(movement_id)
    
    async def get_inventory_movements(
        self,
        filter_command: InventoryMovementFilters,
        offset: int | None = None,
        limit: int | None = None
    ) -> list[InventoryMovement]:
        return await self._inventory_movement_repo.get_with_filters(
            filters_command=filter_command,
            offset=offset,
            limit=limit
        )