from typing import Optional

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.balancing.models.financial_debt import FinancialDebtTable

from app.features.balancing.entities.financial_debt import FinancialDebt


class FinancialDebtMapper(
    BaseMapper[FinancialDebt, FinancialDebtTable]
):

    @staticmethod
    def to_entity(model: FinancialDebtTable) -> FinancialDebt:
        return FinancialDebt(
            id=model.id,
            balance_snapshot_id=model.balance_snapshot_id,
            bank_name=model.bank_name,
            amount=model.amount,
            status=model.status,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_db_model(
        entity: FinancialDebt,
        existing_model: Optional[FinancialDebtTable] = None,
    ) -> FinancialDebtTable:

        if existing_model:
            existing_model.balance_snapshot_id = entity.balance_snapshot_id
            existing_model.bank_name = entity.bank_name
            existing_model.amount = entity.amount
            existing_model.status = entity.status

            return existing_model

        return FinancialDebtTable(
            balance_snapshot_id=entity.balance_snapshot_id,
            bank_name=entity.bank_name,
            amount=entity.amount,
            status=entity.status,
            updated_at=entity.updated_at,
            created_at=entity.created_at,
        )