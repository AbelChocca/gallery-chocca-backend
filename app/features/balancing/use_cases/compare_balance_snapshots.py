from app.features.balancing.calculators.balance_calculator import (
    BalanceCalculator,
)
from app.features.balancing.types.balance_snapshot_types import (
    BalanceComparisonResponse,
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
from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationCategory,
)


class CompareBalanceSnapshotsUseCase:

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
        self._inventory_valuation_service = (
            inventory_valuation_service
        )
        self._other_current_liability_service = (
            other_current_liability_service
        )
        self._balance_calculator = balance_calculator

    async def execute(
        self,
        current_snapshot_id: int,
        previous_snapshot_id: int,
    ) -> BalanceComparisonResponse:

        current_snapshot = (
            await self._balance_snapshot_service.get_by_id(
                current_snapshot_id
            )
        )

        previous_snapshot = (
            await self._balance_snapshot_service.get_by_id(
                previous_snapshot_id
            )
        )

        current_accounts_receivable = (
            await self._accounts_receivable_service.sum_amount(
                balance_snapshot_id=current_snapshot.id,
            )
        )

        current_accounts_payable = (
            await self._accounts_payable_service.sum_amount(
                balance_snapshot_id=current_snapshot.id,
            )
        )

        current_financial_debt = (
            await self._financial_debt_service.sum_amount(
                balance_snapshot_id=current_snapshot.id,
            )
        )

        current_other_current_liabilities = (
            await self._other_current_liability_service.sum_amount(
                balance_snapshot_id=current_snapshot.id,
            )
        )

        current_raw_material = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=current_snapshot.id,
                category=InventoryValuationCategory.RAW_MATERIAL,
            )
        )

        current_work_in_progress = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=current_snapshot.id,
                category=InventoryValuationCategory.WORK_IN_PROGRESS,
            )
        )

        current_finished_goods = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=current_snapshot.id,
                category=InventoryValuationCategory.FINISHED_GOODS,
            )
        )

        current_inventory = (
            self._balance_calculator.calculate_inventory_total(
                raw_material=current_raw_material,
                work_in_progress=current_work_in_progress,
                finished_goods=current_finished_goods,
            )
        )

        current_assets = (
            self._balance_calculator.calculate_current_assets(
                accounts_receivable=current_accounts_receivable,
                inventory=current_inventory,
            )
        )

        current_liabilities = (
            self._balance_calculator.calculate_current_liabilities(
                accounts_payable=current_accounts_payable,
                financial_debt=current_financial_debt,
                other_current_liabilities=(
                    current_other_current_liabilities
                ),
            )
        )

        current_working_capital = (
            self._balance_calculator.calculate_working_capital(
                current_assets=current_assets,
                current_liabilities=current_liabilities,
            )
        )

        previous_accounts_receivable = (
            await self._accounts_receivable_service.sum_amount(
                balance_snapshot_id=previous_snapshot.id,
            )
        )

        previous_accounts_payable = (
            await self._accounts_payable_service.sum_amount(
                balance_snapshot_id=previous_snapshot.id,
            )
        )

        previous_financial_debt = (
            await self._financial_debt_service.sum_amount(
                balance_snapshot_id=previous_snapshot.id,
            )
        )

        previous_other_current_liabilities = (
            await self._other_current_liability_service.sum_amount(
                balance_snapshot_id=previous_snapshot.id,
            )
        )

        previous_raw_material = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=previous_snapshot.id,
                category=InventoryValuationCategory.RAW_MATERIAL,
            )
        )

        previous_work_in_progress = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=previous_snapshot.id,
                category=InventoryValuationCategory.WORK_IN_PROGRESS,
            )
        )

        previous_finished_goods = (
            await self._inventory_valuation_service.sum_amount(
                balance_snapshot_id=previous_snapshot.id,
                category=InventoryValuationCategory.FINISHED_GOODS,
            )
        )

        previous_inventory = (
            self._balance_calculator.calculate_inventory_total(
                raw_material=previous_raw_material,
                work_in_progress=previous_work_in_progress,
                finished_goods=previous_finished_goods,
            )
        )

        previous_assets = (
            self._balance_calculator.calculate_current_assets(
                accounts_receivable=previous_accounts_receivable,
                inventory=previous_inventory,
            )
        )

        previous_liabilities = (
            self._balance_calculator.calculate_current_liabilities(
                accounts_payable=previous_accounts_payable,
                financial_debt=previous_financial_debt,
                other_current_liabilities=(
                    previous_other_current_liabilities
                ),
            )
        )

        previous_working_capital = (
            self._balance_calculator.calculate_working_capital(
                current_assets=previous_assets,
                current_liabilities=previous_liabilities,
            )
        )

        return BalanceComparisonResponse(
            current_snapshot_id=current_snapshot.id,
            previous_snapshot_id=previous_snapshot.id,
            current_period_start=current_snapshot.period_start,
            current_period_end=current_snapshot.period_end,
            previous_period_start=previous_snapshot.period_start,
            previous_period_end=previous_snapshot.period_end,
            current_assets=current_assets,
            previous_assets=previous_assets,
            assets_variation=current_assets - previous_assets,
            liabilities=current_liabilities,
            previous_liabilities=previous_liabilities,
            liabilities_variation=(
                current_liabilities - previous_liabilities
            ),
            working_capital=current_working_capital,
            previous_working_capital=previous_working_capital,
            working_capital_variation=(
                current_working_capital
                - previous_working_capital
            ),
        )
