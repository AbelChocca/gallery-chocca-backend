from app.shared.pagination.dto import PaginatedDTO
from app.shared.pagination.pagination_service import PaginationService

from app.features.balancing.types.balance_snapshot_types import BalanceSnapshotUpdate
from app.features.balancing.entities.balance_snapshot import BalanceSnapshot
from app.features.balancing.repositories.balance_snapshot_repository import (
    BalanceSnapshotRepository,
)
from app.core.exceptions import ValueNotFound

from datetime import datetime, timezone, date

class BalanceSnapshotService:

    def __init__(
        self,
        balance_snapshot_repository: BalanceSnapshotRepository,
        pagination_service: PaginationService,
    ):
        self._balance_snapshot_repository = balance_snapshot_repository
        self._pagination_service = pagination_service

    async def create(
        self,
        entity: BalanceSnapshot,
    ) -> BalanceSnapshot:

        return await self._balance_snapshot_repository.save(entity)

    async def update(
        self,
        entity_id: int,
        dto: BalanceSnapshotUpdate,
    ) -> BalanceSnapshot:

        entity = await self._balance_snapshot_repository.get_by_id(entity_id)

        if entity is None:
            raise ValueNotFound(
                "No se pudo encontrar instantanea del balance",
                {
                    "entity_id": entity_id
                }
            )

        if "period_start" in dto.fields_set:
            entity.period_start = dto.period_start

        if "period_end" in dto.fields_set:
            entity.period_end = dto.period_end

        if "status" in dto.fields_set:
            entity.status = dto.status

        entity.updated_at = datetime.now(timezone.utc)

        return await self._balance_snapshot_repository.save(entity)

    async def get_by_id(
        self,
        snapshot_id: int,
    ) -> BalanceSnapshot:

        return await self._balance_snapshot_repository.get_by_id(
            snapshot_id
        )

    async def get_by_period(
        self,
        period_start: date,
        period_end: date,
    ) -> BalanceSnapshot | None:

        return await self._balance_snapshot_repository.get_by_period(
            period_start=period_start,
            period_end=period_end,
            raises=False,
        )

    async def get_latest(self) -> BalanceSnapshot | None:

        snapshot = await self._balance_snapshot_repository.get_latest()

        if not snapshot:
            raise ValueNotFound(
                "No se encontró la instantánea del saldo.",
            )

        return snapshot

    async def get_all(
        self,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedDTO[BalanceSnapshot]:

        offset = self._pagination_service.get_offset(
            page=page,
            limit=limit,
        )

        items = (
            await self._balance_snapshot_repository.get_all(
                offset=offset,
                limit=limit,
            )
        )

        total_items = await self._balance_snapshot_repository.count()

        total_pages = self._pagination_service.get_total_pages(
            total=total_items,
            limit=limit,
        )

        current_page = self._pagination_service.get_current_page(
            offset=offset,
            limit=limit,
        )

        return PaginatedDTO.create(
            items=items,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )

    async def delete(
        self,
        snapshot_id: int,
    ) -> None:

        await self._balance_snapshot_repository.delete_by_id(
            snapshot_id
        )