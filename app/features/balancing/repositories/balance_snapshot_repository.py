from datetime import date

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import ValueNotFound
from app.infra.db.exceptions import DatabaseException
from app.infra.db.repositories.base_repository import BaseRepository

from app.features.balancing.entities.balance_snapshot import BalanceSnapshot
from app.features.balancing.models.balance_snapshot import (
    BalanceSnapshotTable,
)


class BalanceSnapshotRepository(
    BaseRepository[BalanceSnapshot, BalanceSnapshotTable]
):

    async def get_by_period(
        self,
        period_start: date,
        period_end: date,
        raises: bool = True,
        with_lock: bool = False,
    ) -> BalanceSnapshot | None:

        try:
            statement = (
                select(BalanceSnapshotTable)
                .where(
                    BalanceSnapshotTable.period_start == period_start,
                    BalanceSnapshotTable.period_end == period_end,
                )
            )

            if with_lock:
                statement = statement.with_for_update()

            result = await self._db_session.execute(statement)

            model = result.scalar_one_or_none()

            if not model:
                if not raises:
                    return None

                raise ValueNotFound(
                    "Balance snapshot wasn't found.",
                    {
                        "repository": "postgres_balancesnapshot",
                        "base_model": BalanceSnapshotTable.__name__,
                        "event": "get_by_period",
                        "period_start": period_start,
                        "period_end": period_end,
                    },
                )

            return self._base_mapper.to_entity(model)

        except ValueNotFound:
            raise

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting balance snapshot by period.",
                {
                    "repository": "postgres_balancesnapshot",
                    "base_model": BalanceSnapshotTable.__name__,
                    "event": "get_by_period",
                    "period_start": period_start,
                    "period_end": period_end,
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s

    async def get_all(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[BalanceSnapshot]:

        try:
            statement = (
                select(BalanceSnapshotTable)
                .order_by(
                    BalanceSnapshotTable.period_end.desc(),
                    BalanceSnapshotTable.created_at.desc(),
                )
                .offset(offset)
                .limit(limit)
            )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(model)
                for model in models
            ]

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting balance snapshots.",
                {
                    "repository": "postgres_balancesnapshot",
                    "base_model": BalanceSnapshotTable.__name__,
                    "event": "get_all",
                    "offset": offset,
                    "limit": limit,
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s

    async def count(self) -> int:
        try:
            statement = select(
                func.count(BalanceSnapshotTable.id)
            )

            result = await self._db_session.execute(statement)

            return result.scalar_one()

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while counting balance snapshots.",
                {
                    "repository": "postgres_balancesnapshot",
                    "base_model": BalanceSnapshotTable.__name__,
                    "event": "count",
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s

    async def get_latest(
        self,
        *,
        with_lock: bool = False,
    ) -> BalanceSnapshot | None:

        try:
            statement = (
                select(BalanceSnapshotTable)
                .order_by(
                    BalanceSnapshotTable.period_end.desc(),
                    BalanceSnapshotTable.created_at.desc(),
                )
                .limit(1)
            )

            if with_lock:
                statement = statement.with_for_update()

            result = await self._db_session.execute(statement)

            model = result.scalar_one_or_none()

            if not model:
                return None

            return self._base_mapper.to_entity(model)

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting latest balance snapshot.",
                {
                    "repository": "postgres_balancesnapshot",
                    "base_model": BalanceSnapshotTable.__name__,
                    "event": "get_latest",
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s