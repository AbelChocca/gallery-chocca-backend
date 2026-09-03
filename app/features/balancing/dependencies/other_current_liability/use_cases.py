from app.features.balancing.services.other_current_liability_service import OtherCurrentLiabilityService

from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)

from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.use_cases.get_other_current_liabilities_analysis import (
    GetOtherCurrentLiabilitiesAnalysisUseCase,
)
from app.features.balancing.dependencies.other_current_liability.service import get_other_current_liability_service

from fastapi import Depends

def get_other_current_liabilities_analysis_use_case(
    balance_snapshot_service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
    other_current_liability_service: OtherCurrentLiabilityService = Depends(
        get_other_current_liability_service
    ),
) -> GetOtherCurrentLiabilitiesAnalysisUseCase:
    return GetOtherCurrentLiabilitiesAnalysisUseCase(
        balance_snapshot_service=balance_snapshot_service,
        other_current_liability_service=other_current_liability_service,
    )