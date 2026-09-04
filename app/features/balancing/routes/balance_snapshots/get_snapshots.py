from fastapi import Depends, Query

from app.features.balancing.dependencies.balance_snapshot.service import (
    get_balance_snapshot_service,
)
from app.features.balancing.schemas.balance_snapshot_schema import (
    BalanceSnapshotFilterSchema,
    BalanceSnapshotResponseSchema,
)
from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)
from app.shared.pagination.schema import PaginatedResponseSchema

from app.features.balancing.routes.balance_snapshots.balance_snapshot_router import balance_router

@balance_router.get(
    "/snapshots",
    response_model=PaginatedResponseSchema[BalanceSnapshotResponseSchema]
)
async def get_snapshots(
    filters: BalanceSnapshotFilterSchema = Depends(),
    page: int = Query(..., ge=1),
    limit: int = Query(..., ge=1, le=100),
    service: BalanceSnapshotService = Depends(
        get_balance_snapshot_service
    ),
) -> PaginatedResponseSchema[BalanceSnapshotResponseSchema]:

    filters = filters

    result = await service.get_all(
        page=page,
        limit=limit,
    )

    return PaginatedResponseSchema.model_validate(
        result
    )