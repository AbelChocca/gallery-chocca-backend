from fastapi import Depends, status

from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)
from app.features.balancing.schemas.balance_snapshot_schema import (
    BalanceSnapshotUpdateSchema,
)
from app.features.balancing.types.balance_snapshot_types import BalanceSnapshotUpdate
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)

from app.features.balancing.routes.balance_snapshots.balance_snapshot_router import balance_router


@balance_router.put(
    "/{snapshot_id}",
    status_code=status.HTTP_200_OK,
)
async def update_balance_snapshot(
    snapshot_id: int,
    payload: BalanceSnapshotUpdateSchema,
    service: BalanceSnapshotService = Depends(get_balance_snapshot_service),
):
    update_dto = BalanceSnapshotUpdate(
        period_start=payload.period_start,
        period_end=payload.period_end,
        status=payload.status,
        fields_set=payload.model_fields_set
    )

    return await service.update(
        snapshot_id,
        update_dto,
    )