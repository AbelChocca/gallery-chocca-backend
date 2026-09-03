from typing import Optional

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.balancing.models.other_current_liability import (
    OtherCurrentLiabilityTable,
)

from app.features.balancing.entities.other_current_liability import (
    OtherCurrentLiability,
)


class OtherCurrentLiabilityMapper(
    BaseMapper[
        OtherCurrentLiability,
        OtherCurrentLiabilityTable,
    ]
):

    @staticmethod
    def to_entity(
        model: OtherCurrentLiabilityTable,
    ) -> OtherCurrentLiability:

        return OtherCurrentLiability(
            id=model.id,
            balance_snapshot_id=model.balance_snapshot_id,
            category=model.category,
            description=model.description,
            amount=model.amount,
            status=model.status,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_db_model(
        entity: OtherCurrentLiability,
        existing_model: Optional[OtherCurrentLiabilityTable] = None,
    ) -> OtherCurrentLiabilityTable:

        if existing_model:
            existing_model.balance_snapshot_id = entity.balance_snapshot_id
            existing_model.category = entity.category
            existing_model.description = entity.description
            existing_model.amount = entity.amount
            existing_model.status = entity.status

            return existing_model

        return OtherCurrentLiabilityTable(
            balance_snapshot_id=entity.balance_snapshot_id,
            category=entity.category,
            description=entity.description,
            amount=entity.amount,
            status=entity.status,
            updated_at=entity.updated_at,
            created_at=entity.created_at,
        )