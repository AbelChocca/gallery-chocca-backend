from app.features.balancing.types.other_current_liability_types import (
    OtherCurrentLiabilitiesAnalysisResponse,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.services.other_current_liability_service import (
    OtherCurrentLiabilityService,
)
from app.features.balancing.types.other_current_liability_types import (
    OtherCurrentLiabilityStatus,
)


class GetOtherCurrentLiabilitiesAnalysisUseCase:

    def __init__(
        self,
        balance_snapshot_service: BalanceSnapshotService,
        other_current_liability_service: OtherCurrentLiabilityService,
    ):
        self._balance_snapshot_service = balance_snapshot_service
        self._other_current_liability_service = (
            other_current_liability_service
        )

    async def execute(
        self,
    ) -> OtherCurrentLiabilitiesAnalysisResponse:

        snapshot = (
            await self._balance_snapshot_service.get_latest()
        )

        snapshot_id = snapshot.id

        total_amount = (
            await self._other_current_liability_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        pending_amount = (
            await self._other_current_liability_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=OtherCurrentLiabilityStatus.PENDING,
            )
        )

        partially_paid_amount = (
            await self._other_current_liability_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=OtherCurrentLiabilityStatus.PARTIALLY_PAID,
            )
        )

        paid_amount = (
            await self._other_current_liability_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=OtherCurrentLiabilityStatus.PAID,
            )
        )

        return OtherCurrentLiabilitiesAnalysisResponse(
            total_amount=total_amount,
            pending_amount=pending_amount,
            partially_paid_amount=partially_paid_amount,
            paid_amount=paid_amount,
        )