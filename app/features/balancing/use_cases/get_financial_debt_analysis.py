from app.features.balancing.types.financial_debt_types import (
    FinancialDebtAnalysisResponse,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.features.balancing.services.financial_debt_service import (
    FinancialDebtService,
)
from app.features.balancing.types.financial_debt_types import (
    FinancialDebtStatus,
)
from app.core.exceptions import ValueNotFound

class GetFinancialDebtAnalysisUseCase:

    def __init__(
        self,
        balance_snapshot_service: BalanceSnapshotService,
        financial_debt_service: FinancialDebtService,
    ):
        self._balance_snapshot_service = balance_snapshot_service
        self._financial_debt_service = financial_debt_service

    async def execute(self) -> FinancialDebtAnalysisResponse:

        snapshot = (
            await self._balance_snapshot_service.get_latest()
        )

        if not snapshot:
            raise ValueNotFound(
                "No se encontró la instantánea del saldo.",
            )

        snapshot_id = snapshot.id


        total_amount = (
            await self._financial_debt_service.sum_amount(
                balance_snapshot_id=snapshot_id,
            )
        )

        active_amount = (
            await self._financial_debt_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=FinancialDebtStatus.ACTIVE,
            )
        )

        partially_paid_amount = (
            await self._financial_debt_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=FinancialDebtStatus.PARTIALLY_PAID,
            )
        )

        paid_amount = (
            await self._financial_debt_service.sum_amount(
                balance_snapshot_id=snapshot_id,
                status=FinancialDebtStatus.PAID,
            )
        )

        return FinancialDebtAnalysisResponse(
            total_amount=total_amount,
            active_amount=active_amount,
            partially_paid_amount=partially_paid_amount,
            paid_amount=paid_amount,
        )