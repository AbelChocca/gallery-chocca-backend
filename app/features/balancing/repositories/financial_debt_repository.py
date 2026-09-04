from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException
from app.infra.db.repositories.base_repository import BaseRepository

from app.features.balancing.entities.financial_debt import FinancialDebt
from app.features.balancing.models.financial_debt import FinancialDebtTable
from app.features.balancing.types.financial_debt_types import (
    FinancialDebtStatus,
)


class FinancialDebtRepository(
    BaseRepository[FinancialDebt, FinancialDebtTable]
):

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        bank_name: str | None = None,
        fiscal_year: int | None = None,
        status: FinancialDebtStatus | None = None,
    ) -> list[FinancialDebt]:

        try:
            statement = select(FinancialDebtTable)

            if balance_snapshot_id is not None:
                statement = statement.where(
                    FinancialDebtTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if bank_name is not None:
                statement = statement.where(
                    FinancialDebtTable.bank_name == bank_name
                )

            if fiscal_year is not None:
                statement = statement.where(
                    FinancialDebtTable.fiscal_year == fiscal_year
                )

            if status is not None:
                statement = statement.where(
                    FinancialDebtTable.status == status
                )

            statement = statement.order_by(
                FinancialDebtTable.created_at.desc()
            )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(model)
                for model in models
            ]

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting financial debts.",
                {
                    "repository": "postgres_financialdebt",
                    "base_model": FinancialDebtTable.__name__,
                    "event": "find",
                    "balance_snapshot_id": balance_snapshot_id,
                    "bank_name": bank_name,
                    "fiscal_year": fiscal_year,
                    "status": (
                        status.value
                        if status
                        else None
                    ),
                    "original_error": str(
                        getattr(s, "orig", s)
                    ),
                },
            ) from s

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        bank_name: str | None = None,
        fiscal_year: int | None = None,
        status: FinancialDebtStatus | None = None,
    ) -> Decimal:

        try:
            statement = select(
                func.coalesce(
                    func.sum(
                        FinancialDebtTable.amount
                    ),
                    0,
                )
            )

            if balance_snapshot_id is not None:
                statement = statement.where(
                    FinancialDebtTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if bank_name is not None:
                statement = statement.where(
                    FinancialDebtTable.bank_name == bank_name
                )

            if fiscal_year is not None:
                statement = statement.where(
                    FinancialDebtTable.fiscal_year == fiscal_year
                )

            if status is not None:
                statement = statement.where(
                    FinancialDebtTable.status == status
                )

            result = await self._db_session.execute(statement)

            return result.scalar_one()

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while calculating financial debt total.",
                {
                    "repository": "postgres_financialdebt",
                    "base_model": FinancialDebtTable.__name__,
                    "event": "sum_amount",
                    "balance_snapshot_id": balance_snapshot_id,
                    "bank_name": bank_name,
                    "fiscal_year": fiscal_year,
                    "status": (
                        status.value
                        if status
                        else None
                    ),
                    "original_error": str(
                        getattr(s, "orig", s)
                    ),
                },
            ) from s