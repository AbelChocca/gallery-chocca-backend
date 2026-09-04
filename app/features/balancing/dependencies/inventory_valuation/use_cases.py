from app.features.balancing.services.inventory_valuation_service import InventoryValuationService

from app.features.balancing.calculators.balance_calculator import (
    BalanceCalculator,
    get_balance_calculator,
)
from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.use_cases.get_inventory_valuation_analysis import (
    GetInventoryValuationAnalysisUseCase,
)
from app.features.balancing.dependencies.inventory_valuation.service import get_inventory_valuation_service

from fastapi import Depends

def get_inventory_valuation_analysis_use_case(
    balance_snapshot_service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
    inventory_valuation_service: InventoryValuationService = Depends(
        get_inventory_valuation_service
    ),
    balance_calculator: BalanceCalculator = Depends(
        get_balance_calculator
    ),
) -> GetInventoryValuationAnalysisUseCase:
    return GetInventoryValuationAnalysisUseCase(
        balance_snapshot_service=balance_snapshot_service,
        inventory_valuation_service=inventory_valuation_service,
        balance_calculator=balance_calculator,
    )