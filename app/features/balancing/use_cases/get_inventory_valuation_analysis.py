from app.features.balancing.calculators.balance_calculator import (
    BalanceCalculator,
)
from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationAnalysisResponse,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.services.inventory_valuation_service import (
    InventoryValuationService,
)
from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationCategory,
)


class GetInventoryValuationAnalysisUseCase:

    def __init__(
        self,
        balance_snapshot_service: BalanceSnapshotService,
        inventory_valuation_service: InventoryValuationService,
        balance_calculator: BalanceCalculator,
    ):
        self._balance_snapshot_service = balance_snapshot_service
        self._inventory_valuation_service = (
            inventory_valuation_service
        )
        self._balance_calculator = balance_calculator

    async def execute(
        self,
    ) -> InventoryValuationAnalysisResponse:

        snapshot = (
            await self._balance_snapshot_service.get_latest()
        )

        snapshot_id = snapshot.id

        raw_material_amount = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                category=InventoryValuationCategory.RAW_MATERIAL,
            )
        )

        work_in_progress_amount = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                category=InventoryValuationCategory.WORK_IN_PROGRESS,
            )
        )

        finished_goods_amount = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                category=InventoryValuationCategory.FINISHED_GOODS,
            )
        )

        total_amount = (
            self._balance_calculator.calculate_inventory_total(
                raw_material=raw_material_amount,
                work_in_progress=work_in_progress_amount,
                finished_goods=finished_goods_amount,
            )
        )

        return InventoryValuationAnalysisResponse(
            total_amount=total_amount,
            raw_material_amount=raw_material_amount,
            work_in_progress_amount=work_in_progress_amount,
            finished_goods_amount=finished_goods_amount,
        )