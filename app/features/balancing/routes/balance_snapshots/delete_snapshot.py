from fastapi import Depends, status

from app.features.balancing.routes.balance_snapshots.balance_snapshot_router import balance_router
from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)


@balance_router.delete(
    "/snapshots/{snapshot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_snapshot(
    snapshot_id: int,
    service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
) -> None:

    await service.delete(snapshot_id)