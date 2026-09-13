from sqlalchemy import func, select

from app.features.pricing.entities.coupon_redemption import CouponRedemption
from app.features.pricing.models.coupon_redemption import (
    CouponRedemptionTable,
)
from app.infra.db.repositories.base_repository import BaseRepository


class CouponRedemptionRepository(
    BaseRepository[
        CouponRedemption,
        CouponRedemptionTable,
    ]
):

    async def count_by_coupon_and_customer(
        self,
        *,
        coupon_id: int,
        customer_id: int,
    ) -> int:
        statement = (
            select(func.count(CouponRedemptionTable.id))
            .where(
                CouponRedemptionTable.coupon_id == coupon_id,
                CouponRedemptionTable.customer_id == customer_id,
            )
        )

        result = await self._db_session.execute(statement)

        return result.scalar_one()