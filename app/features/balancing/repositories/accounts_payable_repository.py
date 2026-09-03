from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException
from app.infra.db.repositories.base_repository import BaseRepository

from app.features.balancing.entities.accounts_payable import AccountsPayable
from app.features.balancing.models.accounts_payable import AccountsPayableTable
from app.features.balancing.types.accounts_payable_types import (
    AccountsPayableCostCenter,
    AccountsPayableStatus,
)


class AccountsPayableRepository(
    BaseRepository[
        AccountsPayable,
        AccountsPayableTable,
    ]
):

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        brand: str | None = None,
        cost_center: AccountsPayableCostCenter | None = None,
        status: AccountsPayableStatus | None = None,
    ) -> list[AccountsPayable]:

        try:
            statement = select(AccountsPayableTable)

            if balance_snapshot_id is not None:
                statement = statement.where(
                    AccountsPayableTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if brand is not None:
                statement = statement.where(
                    AccountsPayableTable.brand == brand
                )

            if cost_center is not None:
                statement = statement.where(
                    AccountsPayableTable.cost_center == cost_center
                )

            if status is not None:
                statement = statement.where(
                    AccountsPayableTable.status == status
                )

            statement = statement.order_by(
                AccountsPayableTable.created_at.desc()
            )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(model)
                for model in models
            ]

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting accounts payable.",
                {
                    "repository": "postgres_accountspayable",
                    "base_model": AccountsPayableTable.__name__,
                    "event": "find",
                    "balance_snapshot_id": balance_snapshot_id,
                    "brand": brand,
                    "cost_center": (
                        cost_center.value
                        if cost_center
                        else None
                    ),
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
        brand: str | None = None,
        cost_center: AccountsPayableCostCenter | None = None,
        status: AccountsPayableStatus | None = None,
    ) -> Decimal:

        try:
            statement = select(
                func.coalesce(
                    func.sum(
                        AccountsPayableTable.amount
                    ),
                    0,
                )
            )

            if balance_snapshot_id is not None:
                statement = statement.where(
                    AccountsPayableTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if brand is not None:
                statement = statement.where(
                    AccountsPayableTable.brand == brand
                )

            if cost_center is not None:
                statement = statement.where(
                    AccountsPayableTable.cost_center == cost_center
                )

            if status is not None:
                statement = statement.where(
                    AccountsPayableTable.status == status
                )

            result = await self._db_session.execute(statement)

            return result.scalar_one()

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while calculating accounts payable total.",
                {
                    "repository": "postgres_accountspayable",
                    "base_model": AccountsPayableTable.__name__,
                    "event": "sum_amount",
                    "balance_snapshot_id": balance_snapshot_id,
                    "brand": brand,
                    "cost_center": (
                        cost_center.value
                        if cost_center
                        else None
                    ),
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