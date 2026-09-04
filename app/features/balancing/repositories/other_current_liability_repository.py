from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException
from app.infra.db.repositories.base_repository import BaseRepository

from app.features.balancing.entities.other_current_liability import (
    OtherCurrentLiability,
)
from app.features.balancing.models.other_current_liability import (
    OtherCurrentLiabilityTable,
)
from app.features.balancing.types.other_current_liability_types import (
    OtherCurrentLiabilityStatus,
)


class OtherCurrentLiabilityRepository(
    BaseRepository[
        OtherCurrentLiability,
        OtherCurrentLiabilityTable,
    ]
):

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        category: str | None = None,
        status: OtherCurrentLiabilityStatus | None = None,
    ) -> list[OtherCurrentLiability]:

        try:
            statement = select(OtherCurrentLiabilityTable)

            if balance_snapshot_id is not None:
                statement = statement.where(
                    OtherCurrentLiabilityTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if category is not None:
                statement = statement.where(
                    OtherCurrentLiabilityTable.category == category
                )

            if status is not None:
                statement = statement.where(
                    OtherCurrentLiabilityTable.status == status
                )

            statement = statement.order_by(
                OtherCurrentLiabilityTable.created_at.desc()
            )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(model)
                for model in models
            ]

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting other current liabilities.",
                {
                    "repository": "postgres_othercurrentliability",
                    "base_model": OtherCurrentLiabilityTable.__name__,
                    "event": "find",
                    "balance_snapshot_id": balance_snapshot_id,
                    "category": category,
                    "status": status.value if status else None,
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        category: str | None = None,
        status: OtherCurrentLiabilityStatus | None = None,
    ) -> Decimal:

        try:
            statement = select(
                func.coalesce(
                    func.sum(
                        OtherCurrentLiabilityTable.amount
                    ),
                    0,
                )
            )

            if balance_snapshot_id is not None:
                statement = statement.where(
                    OtherCurrentLiabilityTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if category is not None:
                statement = statement.where(
                    OtherCurrentLiabilityTable.category == category
                )

            if status is not None:
                statement = statement.where(
                    OtherCurrentLiabilityTable.status == status
                )

            result = await self._db_session.execute(statement)

            return result.scalar_one()

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while calculating other current liabilities total.",
                {
                    "repository": "postgres_othercurrentliability",
                    "base_model": OtherCurrentLiabilityTable.__name__,
                    "event": "sum_amount",
                    "balance_snapshot_id": balance_snapshot_id,
                    "category": category,
                    "status": status.value if status else None,
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s