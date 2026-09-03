from fastapi import Depends

from app.features.balancing.dependencies.balance_snapshot.use_cases import (
    get_current_balance_use_case,
)
from app.features.balancing.use_cases.get_current_balance import (
    GetCurrentBalanceUseCase,
)

from app.features.balancing.routes.balance_snapshots.balance_snapshot_router import balance_router
from app.features.balancing.schemas.balance_snapshot_schema import BalanceResponseSchema


@balance_router.get(
    "/snapshots/current",
    response_model=BalanceResponseSchema,
)
async def get_current_snapshot(
    use_case: GetCurrentBalanceUseCase = Depends(
        get_current_balance_use_case
    ),
) -> BalanceResponseSchema:

    balance = await use_case.execute()

    return BalanceResponseSchema.model_validate(balance)

