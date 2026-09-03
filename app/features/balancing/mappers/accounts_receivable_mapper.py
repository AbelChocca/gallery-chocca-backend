from typing import Optional

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.balancing.models.accounts_receivable import (
    AccountsReceivableTable,
)

from app.features.balancing.entities.accounts_receivable import (
    AccountsReceivable,
)


class AccountsReceivableMapper(
    BaseMapper[AccountsReceivable, AccountsReceivableTable]
):

    @staticmethod
    def to_entity(model: AccountsReceivableTable) -> AccountsReceivable:
        return AccountsReceivable(
            id=model.id,
            balance_snapshot_id=model.balance_snapshot_id,
            brand=model.brand,
            entity_name=model.entity_name,
            location=model.location,
            amount=model.amount,
            status=model.status,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_db_model(
        entity: AccountsReceivable,
        existing_model: Optional[AccountsReceivableTable] = None,
    ) -> AccountsReceivableTable:

        if existing_model:
            existing_model.balance_snapshot_id = entity.balance_snapshot_id
            existing_model.brand = entity.brand
            existing_model.entity_name = entity.entity_name
            existing_model.location = entity.location
            existing_model.amount = entity.amount
            existing_model.status = entity.status

            return existing_model

        return AccountsReceivableTable(
            balance_snapshot_id=entity.balance_snapshot_id,
            brand=entity.brand,
            entity_name=entity.entity_name,
            location=entity.location,
            amount=entity.amount,
            status=entity.status,
            updated_at=entity.updated_at,
            created_at=entity.created_at,
        )