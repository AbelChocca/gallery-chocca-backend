from fastapi import Depends

from app.features.balancing.dependencies.balance_snapshot.use_cases import (
    get_balance_snapshot_use_case,
)
from app.features.balancing.use_cases.get_balance_snapshot import (
    GetBalanceSnapshotUseCase,
)
from app.features.balancing.schemas.balance_snapshot_schema import BalanceResponseSchema
from app.features.balancing.routes.balance_snapshots.balance_snapshot_router import balance_router


@balance_router.get(
    "/snapshots/{snapshot_id}",
    response_model=BalanceResponseSchema,
)
async def get_snapshot(
    snapshot_id: int,
    use_case: GetBalanceSnapshotUseCase = Depends(
        get_balance_snapshot_use_case
    ),
) -> BalanceResponseSchema:

    balance = await use_case.execute(snapshot_id)

    return BalanceResponseSchema.model_validate(balance)