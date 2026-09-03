from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException
from app.infra.db.repositories.base_repository import BaseRepository

from app.features.balancing.entities.accounts_receivable import (
    AccountsReceivable,
)
from app.features.balancing.models.accounts_receivable import (
    AccountsReceivableTable,
)
from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableStatus,
)


class AccountsReceivableRepository(
    BaseRepository[
        AccountsReceivable,
        AccountsReceivableTable,
    ]
):

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        brand: str | None = None,
        entity_name: str | None = None,
        location: str | None = None,
        status: AccountsReceivableStatus | None = None,
    ) -> list[AccountsReceivable]:

        try:
            statement = select(AccountsReceivableTable)

            if balance_snapshot_id is not None:
                statement = statement.where(
                    AccountsReceivableTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if brand is not None:
                statement = statement.where(
                    AccountsReceivableTable.brand == brand
                )

            if entity_name is not None:
                statement = statement.where(
                    AccountsReceivableTable.entity_name == entity_name
                )

            if location is not None:
                statement = statement.where(
                    AccountsReceivableTable.location == location
                )

            if status is not None:
                statement = statement.where(
                    AccountsReceivableTable.status == status
                )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(row)
                for row in models
            ]

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "No se pudieron obtener las cuentas por cobrar."
            ) from exc

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        brand: str | None = None,
        entity_name: str | None = None,
        location: str | None = None,
        status: AccountsReceivableStatus | None = None,
    ) -> Decimal:

        try:
            statement = select(
                func.coalesce(
                    func.sum(AccountsReceivableTable.amount),
                    Decimal("0"),
                )
            )

            if balance_snapshot_id is not None:
                statement = statement.where(
                    AccountsReceivableTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if brand is not None:
                statement = statement.where(
                    AccountsReceivableTable.brand == brand
                )

            if entity_name is not None:
                statement = statement.where(
                    AccountsReceivableTable.entity_name == entity_name
                )

            if location is not None:
                statement = statement.where(
                    AccountsReceivableTable.location == location
                )

            if status is not None:
                statement = statement.where(
                    AccountsReceivableTable.status == status
                )

            result = await self._db_session.execute(statement)

            return result.scalar_one()

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "No se pudo calcular el total de cuentas por cobrar."
            ) from exc