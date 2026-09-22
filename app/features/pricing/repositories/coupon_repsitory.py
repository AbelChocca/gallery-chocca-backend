from sqlalchemy import select

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