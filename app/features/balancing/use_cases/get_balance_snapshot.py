from app.features.balancing.types.balance_snapshot_types import (
    BalanceResponse,
)
from app.features.balancing.services.accounts_payable_service import (
    AccountsPayableService,
)
from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
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
)
from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationCategory,
)

class GetBalanceSnapshotUseCase:

    def __init__(
        self,
        balance_snapshot_service: BalanceSnapshotService,
        accounts_receivable_service: AccountsReceivableService,
        accounts_payable_service: AccountsPayableService,
        financial_debt_service: FinancialDebtService,
        inventory_valuation_service: InventoryValuationService,
        other_current_liability_service: OtherCurrentLiabilityService,
        balance_calculator: BalanceCalculator,
    ):
        self._balance_snapshot_service = balance_snapshot_service
        self._accounts_receivable_service = accounts_receivable_service
        self._accounts_payable_service = accounts_payable_service
        self._financial_debt_service = financial_debt_service
        self._inventory_valuation_service = inventory_valuation_service
        self._other_current_liability_service = (
            other_current_liability_service
        )
        self._balance_calculator = balance_calculator

    async def execute(
        self,
        snapshot_id: int,
    ) -> BalanceResponse:

        snapshot = await self._balance_snapshot_service.get_by_id(
            snapshot_id
        )

        snapshot_id = snapshot.id

        accounts_receivable = (
            await self._accounts_receivable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        accounts_payable = (
            await self._accounts_payable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        financial_debt = (
            await self._financial_debt_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        other_current_liabilities = (
            await self._other_current_liability_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        raw_material = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                category=InventoryValuationCategory.RAW_MATERIAL,
            )
        )

        work_in_progress = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                category=InventoryValuationCategory.WORK_IN_PROGRESS,
            )
        )

        finished_goods = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                category=InventoryValuationCategory.FINISHED_GOODS,
            )
        )

        inventory = self._balance_calculator.calculate_inventory_total(
            raw_material=raw_material,
            work_in_progress=work_in_progress,
            finished_goods=finished_goods,
        )

        current_assets = self._balance_calculator.calculate_current_assets(
            accounts_receivable=accounts_receivable,
            inventory_valuation=inventory,
        )

        current_liabilities = (
            self._balance_calculator.calculate_current_liabilities(
                accounts_payable=accounts_payable,
                financial_debt=financial_debt,
                other_current_liabilities=other_current_liabilities,
            )
        )

        working_capital = (
            self._balance_calculator.calculate_working_capital(
                current_assets=current_assets,
                current_liabilities=current_liabilities,
            )
        )

        return BalanceResponse(
            id=snapshot.id,
            period_start=snapshot.period_start,
            period_end=snapshot.period_end,
            status=snapshot.status,
            created_at=snapshot.created_at,
            total_current_assets=current_assets,
            total_current_liabilities=current_liabilities,
            working_capital=working_capital,
            accounts_receivable=accounts_receivable,
            raw_material=raw_material,
            work_in_progress=work_in_progress,
            finished_goods=finished_goods,
            accounts_payable=accounts_payable,
            financial_debt=financial_debt,
            other_current_liabilities=other_current_liabilities,
        )