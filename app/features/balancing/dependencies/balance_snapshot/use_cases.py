from fastapi import Depends

from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)

from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)

from app.features.balancing.services.accounts_payable_service import (
    AccountsPayableService,
)

from app.features.balancing.services.financial_debt_service import (
    FinancialDebtService,
)

from app.features.balancing.services.inventory_valuation_service import (
    InventoryValuationService,
)

from app.features.balancing.services.other_current_liability_service import (
    OtherCurrentLiabilityService,
)

from app.features.balancing.calculators.balance_calculator import (
    BalanceCalculator,
    get_balance_calculator
)

from app.features.balancing.use_cases.get_current_balance import (
    GetCurrentBalanceUseCase,
)

from app.features.balancing.use_cases.compare_balance_snapshots import (
    CompareBalanceSnapshotsUseCase,
)
from app.features.balancing.dependencies.accounts_receivable.service import get_accounts_receivable_service
from app.features.balancing.dependencies.accounts_payable.service import get_accounts_payable_service
from app.features.balancing.dependencies.financial_debt.service import get_financial_debt_service
from app.features.balancing.dependencies.inventory_valuation.service import get_inventory_valuation_service
from app.features.balancing.dependencies.other_current_liability.service import get_other_current_liability_service

from app.features.balancing.use_cases.get_balance_snapshot import (
    GetBalanceSnapshotUseCase,
)

from fastapi import Depends

from app.features.balancing.dependencies.balance_snapshot.service import get_balance_snapshot_service

def get_compare_balance_snapshots_use_case(
    service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
    accounts_receivable: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
    accounts_payable: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
    financial_debt: FinancialDebtService = Depends(get_financial_debt_service),
    inventory_valuation: InventoryValuationService = Depends(get_inventory_valuation_service),
    other_current_liability: OtherCurrentLiabilityService = Depends(get_other_current_liability_service),
    calculator: BalanceCalculator = Depends(get_balance_calculator)
) -> CompareBalanceSnapshotsUseCase:
    return CompareBalanceSnapshotsUseCase(
        balance_snapshot_service=service,
        accounts_receivable_service=accounts_receivable,
        accounts_payable_service=accounts_payable,
        financial_debt_service=financial_debt,
        inventory_valuation_service=inventory_valuation,
        other_current_liability_service=other_current_liability,
        balance_calculator=calculator
    )

def get_current_balance_use_case(
    service: BalanceSnapshotService = Depends(
            get_balance_snapshot_service
        ),
    accounts_receivable: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
    accounts_payable: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
    financial_debt: FinancialDebtService = Depends(
        get_financial_debt_service
    ),
    inventory_valuation: InventoryValuationService = Depends(
        get_inventory_valuation_service
    ),
    other_current_liability: OtherCurrentLiabilityService = Depends(
        get_other_current_liability_service
    ),
    calculator: BalanceCalculator = Depends(
        get_balance_calculator
    ),
) -> GetCurrentBalanceUseCase:
    return GetCurrentBalanceUseCase(
        balance_snapshot_service=service,
        accounts_receivable_service=accounts_receivable,
        accounts_payable_service=accounts_payable,
        financial_debt_service=financial_debt,
        inventory_valuation_service=inventory_valuation,
        other_current_liability_service=other_current_liability,
        balance_calculator=calculator,
    )

def get_balance_snapshot_use_case(
    balance_snapshot_service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
    accounts_receivable: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
    accounts_payable: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
    financial_debt: FinancialDebtService = Depends(
        get_financial_debt_service
    ),
    inventory_valuation: InventoryValuationService = Depends(
        get_inventory_valuation_service
    ),
    other_current_liability: OtherCurrentLiabilityService = Depends(
        get_other_current_liability_service
    ),
    calculator: BalanceCalculator = Depends(
        get_balance_calculator
    ),
) -> GetBalanceSnapshotUseCase:

    return GetBalanceSnapshotUseCase(
        balance_snapshot_service=balance_snapshot_service,
        accounts_receivable_service=accounts_receivable,
        accounts_payable_service=accounts_payable,
        financial_debt_service=financial_debt,
        inventory_valuation_service=inventory_valuation,
        other_current_liability_service=other_current_liability,
        balance_calculator=calculator,
    )