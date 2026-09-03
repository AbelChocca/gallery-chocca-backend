from app.features.balancing.services.accounts_receivable_service import AccountsReceivableService

from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.use_cases.get_accounts_receivable_analysis import (
    GetAccountsReceivableAnalysisUseCase,
)
from app.features.balancing.dependencies.accounts_receivable.service import get_accounts_receivable_service

from fastapi import Depends

def get_accounts_receivable_analysis_use_case(
    balance_snapshot_service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
    accounts_receivable_service: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
) -> GetAccountsReceivableAnalysisUseCase:
    return GetAccountsReceivableAnalysisUseCase(
        balance_snapshot_service=balance_snapshot_service,
        accounts_receivable_service=accounts_receivable_service,
    )