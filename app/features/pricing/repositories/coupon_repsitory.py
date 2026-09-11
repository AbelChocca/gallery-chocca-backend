from sqlalchemy import select

from app.features.pricing.entities.coupon import Coupon
from app.features.pricing.models.coupon import CouponTable
from app.infra.db.repositories.base_repository import BaseRepository


class CouponRepository(
    BaseRepository[Coupon, CouponTable]
):

    async def get_by_id(
        self,
        coupon_id: int,
    ) -> Coupon | None:
        return await super().get_by_id(coupon_id)

    async def get_by_code(
        self,
        *,
        code: str,
    ) -> Coupon | None:
        statement = (
            select(CouponTable)
            .where(
                CouponTable.code == code,
            )
        )

        result = await self._db_session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._base_mapper.to_entity(model)