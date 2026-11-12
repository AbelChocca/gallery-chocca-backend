
from app.features.balancing.repositories.balance_snapshot_repository import (
    BalanceSnapshotRepository,
)
from app.features.balancing.repositories.accounts_receivable_repository import (
    AccountsReceivableRepository,
)
from app.features.balancing.repositories.accounts_payable_repository import (
    AccountsPayableRepository,
)
from app.features.balancing.repositories.financial_debt_repository import (
    FinancialDebtRepository,
)
from app.features.balancing.repositories.inventory_valuation_repository import (
    InventoryValuationRepository,
)
from app.features.balancing.repositories.other_current_liability_repository import (
    OtherCurrentLiabilityRepository,
)

from app.features.balancing.mappers.balance_snapshot_mapper import (
    BalanceSnapshotMapper,
)
from app.features.balancing.mappers.accounts_receivable_mapper import (
    AccountsReceivableMapper,
)
from app.features.balancing.mappers.accounts_payable_mapper import (
    AccountsPayableMapper,
)
from app.features.balancing.mappers.financial_debt_mapper import (
    FinancialDebtMapper,
)
from app.features.balancing.mappers.inventory_valuation_mapper import (
    InventoryValuationMapper,
)
from app.features.balancing.mappers.other_current_liability_mapper import (
    OtherCurrentLiabilityMapper,
)

from app.features.balancing.models.balance_snapshot import (
    BalanceSnapshotTable,
)
from app.features.balancing.models.accounts_receivable import (
    AccountsReceivableTable,
)
from app.features.balancing.models.accounts_payable import (
    AccountsPayableTable,
)
from app.features.balancing.models.financial_debt import (
    FinancialDebtTable,
)
from app.features.balancing.models.inventory_valuation import (
    InventoryValuationTable,
)
from app.features.balancing.models.other_current_liability import (
    OtherCurrentLiabilityTable,
)


class BalancingRepositoriesMixin:

    @property
    def accounts_receivable(
        self,
    ) -> AccountsReceivableRepository:
        return self._get_or_create(
            "accounts_receivable",
            lambda: AccountsReceivableRepository(
                self.session,
                AccountsReceivableMapper,
                AccountsReceivableTable,
            ),
        )

    @property
    def accounts_payable(
        self,
    ) -> AccountsPayableRepository:
        return self._get_or_create(
            "accounts_payable",
            lambda: AccountsPayableRepository(
                self.session,
                AccountsPayableMapper,
                AccountsPayableTable,
            ),
        )

    @property
    def financial_debts(
        self,
    ) -> FinancialDebtRepository:
        return self._get_or_create(
            "financial_debts",
            lambda: FinancialDebtRepository(
                self.session,
                FinancialDebtMapper,
                FinancialDebtTable,
            ),
        )

    @property
    def inventory_valuations(
        self,
    ) -> InventoryValuationRepository:
        return self._get_or_create(
            "inventory_valuations",
            lambda: InventoryValuationRepository(
                self.session,
                InventoryValuationMapper,
                InventoryValuationTable,
            ),
        )

    @property
    def other_current_liabilities(
        self,
    ) -> OtherCurrentLiabilityRepository:
        return self._get_or_create(
            "other_current_liabilities",
            lambda: OtherCurrentLiabilityRepository(
                self.session,
                OtherCurrentLiabilityMapper,
                OtherCurrentLiabilityTable,
            ),
        )

    @property
    def balance_snapshots(
        self,
    ) -> BalanceSnapshotRepository:
        return self._get_or_create(
            "balance_snapshots",
            lambda: BalanceSnapshotRepository(
                self.session,
                BalanceSnapshotMapper,
                BalanceSnapshotTable,
            ),
        )
