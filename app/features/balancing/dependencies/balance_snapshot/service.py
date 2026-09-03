from fastapi import Depends

from app.infra.db.uow.unit_of_work import UnitOfWork

from app.features.balancing.repositories.balance_snapshot_repository import (
    BalanceSnapshotRepository,
)

from app.features.balancing.services.balance_snapshot_service import (
    BalanceSnapshotService,
)

from app.infra.db.uow.dependency import get_uow

from app.shared.pagination.pagination_service import PaginationService, get_pagination_service

def get_balance_snapshot_repository(
    uow: UnitOfWork = Depends(get_uow),
) -> BalanceSnapshotRepository:
    return uow.balance_snapshots

def get_balance_snapshot_service(
    repository: BalanceSnapshotRepository = Depends(
        get_balance_snapshot_repository
    ),
    pagination: PaginationService = Depends(get_pagination_service)
) -> BalanceSnapshotService:
    return BalanceSnapshotService(
        balance_snapshot_repository=repository,
        pagination_service=pagination
    )