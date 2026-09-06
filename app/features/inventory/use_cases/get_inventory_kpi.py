from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_movement_service import InventoryMovementService

from app.features.inventory.types.inventory_movement import InventoryOwnerType
from app.features.inventory.dtos.inventory import InventoryKPIsDTO
from app.features.inventory.entities.inventory_movement_entity import InventoryMovement
from datetime import datetime, timedelta, timezone
from decimal import Decimal

class GetInventoryKPIsUseCase:

    def __init__(
        self,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
    ) -> None:
        self._inventory_service = inventory_service
        self._inventory_movement_service = inventory_movement_service

    async def execute(
        self,
        *,
        owner_type: InventoryOwnerType,
        current_location_id: int,
    ) -> InventoryKPIsDTO:

        inventories = await (
            self._inventory_service
            .get_inventory_for_kpis(
                owner_type=owner_type,
                current_location_id=current_location_id,
            )
        )

        inventory_value = Decimal("0")
        total_items = len(inventories)
        items_below_minimum = 0
        reserved_items = 0
        reserved_quantity = Decimal("0")

        for inventory in inventories:

            if inventory.unit_price is not None:
                inventory_value += (
                    inventory.quantity
                    * inventory.unit_price
                )

            available_quantity = (
                inventory.quantity
                - inventory.reserved_quantity
            )

            if available_quantity <= inventory.minimum_stock:
                items_below_minimum += 1

            if inventory.reserved_quantity > 0:
                reserved_items += 1
                reserved_quantity += inventory.reserved_quantity

        owner_ids = [
            inventory.owner_id
            for inventory in inventories
        ]

        last_movements = await (
            self._inventory_movement_service
            .get_last_movements_by_owner_ids(
                owner_type=owner_type,
                owner_ids=owner_ids,
            )
        )

        items_without_movement = self._count_items_without_movement(
            owner_ids=owner_ids,
            last_movements=last_movements,
        )

        movement_summary = await (
            self._inventory_movement_service
            .get_movement_summary(
                owner_type=owner_type,
                owner_ids=owner_ids,
                location_id=current_location_id,
            )
        )

        return InventoryKPIsDTO(
            inventory_value=inventory_value,
            total_items=total_items,
            items_below_minimum=items_below_minimum,
            reserved_items=reserved_items,
            reserved_quantity=reserved_quantity,
            items_without_movement=items_without_movement,
            total_entries=movement_summary.total_entries,
            total_exits=movement_summary.total_exits,
        )

    def _count_items_without_movement(
        self,
        *,
        owner_ids: list[int],
        last_movements: dict[int, InventoryMovement],
        threshold_days: int = 30,
    ) -> int:

        now = datetime.now(timezone.utc)
        threshold = now - timedelta(days=threshold_days)

        return sum(
            1
            for owner_id in owner_ids
            if (
                owner_id not in last_movements
                or last_movements[owner_id].created_at < threshold
            )
        )