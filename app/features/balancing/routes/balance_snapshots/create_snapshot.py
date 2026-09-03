from fastapi import Depends, status

from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)
from app.features.balancing.entities.balance_snapshot import BalanceSnapshot
from app.features.balancing.schemas.balance_snapshot_schema import (
    BalanceSnapshotCreateSchema,
    BalanceSnapshotResponseSchema,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)

from app.features.balancing.routes.balance_snapshots.balance_snapshot_router import balance_router

@balance_router.post(
    "/snapshots",
    response_model=BalanceSnapshotResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_snapshot(
    schema: BalanceSnapshotCreateSchema,
    service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
) -> BalanceSnapshotResponseSchema:

    entity = BalanceSnapshot(
        period_start=schema.period_start,
        period_end=schema.period_end,
        status=schema.status,

    )

    snapshot = await service.create(entity)

    return BalanceSnapshotResponseSchema.model_validate(snapshot)