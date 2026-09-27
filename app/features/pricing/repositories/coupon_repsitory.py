from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.exceptions import ValueNotFound
from app.infra.db.exceptions import DatabaseException

from app.features.pricing.entities.coupon import Coupon
from app.features.pricing.models.coupon import CouponTable
from app.infra.db.repositories.base_repository import BaseRepository


class CouponRepository(
    BaseRepository[
        Coupon,
        CouponTable,
    ]
):

    async def get_by_code(
        self,
        *,
        code: str,
        with_lock: bool = False,
    ) -> Coupon | None:

        statement = (
            select(CouponTable)
            .where(
                CouponTable.code == code,
            )
        )

        if with_lock:
            statement = statement.with_for_update()

        result = await self._db_session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._base_mapper.to_entity(model)

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[Coupon]:

        statement = (
            select(CouponTable)
            .where(
                CouponTable.promotion_id == promotion_id,
            )
            .order_by(
                CouponTable.created_at.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def save(
        self,
        entity: Coupon,
        flush: bool = True,
    ) -> Coupon:
        try:
            if entity.id is None:
                model = self._base_mapper.to_db_model(
                    entity
                )
            else:
                existing_model = (
                    await self._get_model_by_id_non_raise(
                        entity.id
                    )
                )

                model = self._base_mapper.to_db_model(
                    entity=entity,
                    existing_model=existing_model,
                )

            self._db_session.add(model)

            if flush:
                await self._db_session.flush()
                await self._db_session.refresh(model)

            return self._base_mapper.to_entity(
                model
            )

        except IntegrityError as exc:
            original_error = str(exc.orig)

            if (
                "coupons_promotion_id_fkey"
                in original_error
            ):
                raise ValueNotFound(
                    "La promoción asociada no fue encontrada.",
                    {
                        "repository": "postgres_coupon",
                        "event": "save",
                        "promotion_id": entity.promotion_id,
                    },
                ) from exc

            raise DatabaseException(
                "Integrity constraint violation",
                {
                    "repository": "postgres_coupon",
                    "base_model": self._base_model.__name__,
                    "db_error_code": "integrity_error",
                    "event": "save",
                    "original_error": original_error,
                },
            ) from exc

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "Postgres error while saving",
                {
                    "repository": "postgres_coupon",
                    "base_model": self._base_model.__name__,
                    "event": "save",
                    "original_error": str(
                        getattr(exc, "orig", exc)
                    ),
                },
            ) from exc