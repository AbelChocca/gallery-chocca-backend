from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_movement_service import InventoryMovementService

from app.features.inventory.types.inventory_movement import InventoryOwnerType, InventoryMovementType
from app.features.inventory.types.inventory import InventoryAnalysisStatus
from app.features.inventory.dtos.inventory_movements import InventoryMovementFilters
from app.features.inventory.dtos.inventory import InventoryAnalysisDTO
from app.features.inventory.entities.inventory_movement_entity import InventoryMovement
from app.core.exceptions import ValueNotFound

from datetime import datetime, timedelta, timezone
from decimal import Decimal



class GetInventoryAnalysisUseCase:

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
        owner_id: int,
    ) -> InventoryAnalysisDTO:

        inventories = await (
            self._inventory_service
            .get_owner_inventories(
                owner_type=owner_type,
                owner_id=owner_id,
            )
        )

        if not inventories:
            raise ValueNotFound(
                "Inventory not found."
            )

        now = datetime.now(timezone.utc)

        date_7d = now - timedelta(days=7)
        date_30d = now - timedelta(days=30)

        # Movimientos históricos
        movements = await (
            self._inventory_movement_service
            .get_inventory_movements(
                filter_command=InventoryMovementFilters(
                    owner_type=owner_type,
                    owner_id=owner_id,
                )
            )
        )

        consumption_7d = Decimal("0")
        consumption_30d = Decimal("0")

        for movement in movements:

            if not self._is_consumption(movement):
                continue

            if movement.created_at >= date_30d:
                consumption_30d += abs(movement.quantity)

                if movement.created_at >= date_7d:
                    consumption_7d += abs(movement.quantity)

        available_stock = sum(
            inventory.quantity -
            inventory.reserved_quantity
            for inventory in inventories
        )

        daily_consumption = (
            consumption_30d / Decimal("30")
            if consumption_30d > 0
            else None
        )

        coverage_days = (
            (available_stock / daily_consumption).quantize(
                Decimal("0.01")
            )
            if daily_consumption
            else None
        )

        status = self._calculate_status(
            coverage_days=coverage_days,
        )

        return InventoryAnalysisDTO(
            coverage_days=coverage_days,
            status=status,
            consumption_7d=consumption_7d,
            consumption_30d=consumption_30d,
        )

    def _is_consumption(
        self,
        movement: InventoryMovement,
    ) -> bool:

        return movement.type == InventoryMovementType.USAGE

    def _calculate_status(
        self,
        coverage_days: Decimal | None,
    ) -> InventoryAnalysisStatus:

        if coverage_days is None:
            return InventoryAnalysisStatus.NO_CONSUMPTION

        if coverage_days <= Decimal("3"):
            return InventoryAnalysisStatus.CRITICAL

        if coverage_days <= Decimal("7"):
            return InventoryAnalysisStatus.ATTENTION

        return InventoryAnalysisStatus.HEALTHY