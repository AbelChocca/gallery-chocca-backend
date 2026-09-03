from app.features.balancing.services.accounts_payable_service import AccountsPayableService

from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)

from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.use_cases.get_accounts_payable_analysis import (
    GetAccountsPayableAnalysisUseCase,
)
from app.features.balancing.dependencies.accounts_payable.service import get_accounts_payable_service

from fastapi import Depends

def get_accounts_payable_analysis_use_case(
    balance_snapshot_service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
    accounts_payable_service: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
) -> GetAccountsPayableAnalysisUseCase:
    return GetAccountsPayableAnalysisUseCase(
        balance_snapshot_service=balance_snapshot_service,
        accounts_payable_service=accounts_payable_service,
    )