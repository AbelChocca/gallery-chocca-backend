from typing import Optional

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.balancing.models.balance_snapshot import BalanceSnapshotTable

from app.features.balancing.entities.balance_snapshot import BalanceSnapshot


class BalanceSnapshotMapper(BaseMapper[BalanceSnapshot, BalanceSnapshotTable]):

    @staticmethod
    def to_entity(model: BalanceSnapshotTable) -> BalanceSnapshot:
        return BalanceSnapshot(
            id=model.id,
            period_start=model.period_start,
            period_end=model.period_end,
            status=model.status,
            created_at=model.created_at,
        )
    
    @staticmethod
    def to_db_model(
        entity: BalanceSnapshot,
        existing_model: Optional[BalanceSnapshotTable] = None,
    ) -> BalanceSnapshotTable:

        if existing_model:
            existing_model.period_start = entity.period_start
            existing_model.period_end = entity.period_end
            existing_model.status = entity.status

            return existing_model

        return BalanceSnapshotTable(
            period_start=entity.period_start,
            period_end=entity.period_end,
            status=entity.status,
            created_at=entity.created_at,
        )