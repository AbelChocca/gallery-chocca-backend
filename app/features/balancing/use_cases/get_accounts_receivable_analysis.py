from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableAnalysisResponse,
)
from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableStatus,
)


class GetAccountsReceivableAnalysisUseCase:

    def __init__(
        self,
        balance_snapshot_service: BalanceSnapshotService,
        accounts_receivable_service: AccountsReceivableService,
    ):
        self._balance_snapshot_service = balance_snapshot_service
        self._accounts_receivable_service = (
            accounts_receivable_service
        )

    async def execute(self) -> AccountsReceivableAnalysisResponse:

        snapshot = (
            await self._balance_snapshot_service.get_latest()
        )

        snapshot_id = snapshot.id

        total_amount = (
            await self._accounts_receivable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        pending_amount = (
            await self._accounts_receivable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=AccountsReceivableStatus.PENDING,
            )
        )

        partially_collected_amount = (
            await self._accounts_receivable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=AccountsReceivableStatus.PARTIALLY_COLLECTED,
            )
        )

        collected_amount = (
            await self._accounts_receivable_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=AccountsReceivableStatus.COLLECTED,
            )
        )

        return AccountsReceivableAnalysisResponse(
            total_amount=total_amount,
            pending_amount=pending_amount,
            partially_collected_amount=partially_collected_amount,
            collected_amount=collected_amount,
        )