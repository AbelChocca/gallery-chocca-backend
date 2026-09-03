from typing import Optional

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.balancing.models.accounts_payable import AccountsPayableTable

from app.features.balancing.entities.accounts_payable import AccountsPayable


class AccountsPayableMapper(
    BaseMapper[AccountsPayable, AccountsPayableTable]
):

    @staticmethod
    def to_entity(model: AccountsPayableTable) -> AccountsPayable:
        return AccountsPayable(
            id=model.id,
            balance_snapshot_id=model.balance_snapshot_id,
            brand=model.brand,
            entity_name=model.entity_name,
            cost_center=model.cost_center,
            amount=model.amount,
            status=model.status,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_db_model(
        entity: AccountsPayable,
        existing_model: Optional[AccountsPayableTable] = None,
    ) -> AccountsPayableTable:

        if existing_model:
            existing_model.balance_snapshot_id = entity.balance_snapshot_id
            existing_model.brand = entity.brand
            existing_model.entity_name = entity.entity_name
            existing_model.cost_center = entity.cost_center
            existing_model.amount = entity.amount
            existing_model.status = entity.status

            return existing_model

        return AccountsPayableTable(
            balance_snapshot_id=entity.balance_snapshot_id,
            brand=entity.brand,
            entity_name=entity.entity_name,
            cost_center=entity.cost_center,
            amount=entity.amount,
            status=entity.status,
            updated_at=entity.updated_at,
            created_at=entity.created_at,
        )