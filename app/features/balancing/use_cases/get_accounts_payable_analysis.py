from app.features.balancing.types.accounts_payable_types import (
    AccountsPayableAnalysisResponse,
)
from app.features.balancing.services.accounts_payable_service import (
    AccountsPayableService,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.types.accounts_payable_types import (
    AccountsPayableStatus,
)


class GetAccountsPayableAnalysisUseCase:

    def __init__(
        self,
        balance_snapshot_service: BalanceSnapshotService,
        accounts_payable_service: AccountsPayableService,
    ):
        self._balance_snapshot_service = balance_snapshot_service
        self._accounts_payable_service = accounts_payable_service

    async def execute(self) -> AccountsPayableAnalysisResponse:

        snapshot = (
            await self._balance_snapshot_service.get_latest()
        )

        snapshot_id = snapshot.id

        total_amount = (
            await self._accounts_payable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        pending_amount = (
            await self._accounts_payable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=AccountsPayableStatus.PENDING,
            )
        )

        partially_paid_amount = (
            await self._accounts_payable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=AccountsPayableStatus.PARTIALLY_PAID,
            )
        )

        paid_amount = (
            await self._accounts_payable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=AccountsPayableStatus.PAID,
            )
        )

        return AccountsPayableAnalysisResponse(
            total_amount=total_amount,
            pending_amount=pending_amount,
            partially_paid_amount=partially_paid_amount,
            paid_amount=paid_amount,
        )