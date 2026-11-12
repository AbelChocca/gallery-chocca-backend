from sqlalchemy import func, select

from app.features.pricing.entities.coupon_redemption import (
    CouponRedemption,
)
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
            select(
                func.count(CouponRedemptionTable.id)
            )
            .where(
                CouponRedemptionTable.coupon_id == coupon_id,
                CouponRedemptionTable.customer_id == customer_id,
            )
        )

        result = await self._db_session.execute(statement)

        return result.scalar_one()

    async def count_by_coupon(
        self,
        *,
        coupon_id: int,
    ) -> int:

        statement = (
            select(
                func.count(CouponRedemptionTable.id)
            )
            .where(
                CouponRedemptionTable.coupon_id == coupon_id,
            )
        )

        result = await self._db_session.execute(statement)

        return result.scalar_one()

    async def get_by_coupon(
        self,
        *,
        coupon_id: int,
    ) -> list[CouponRedemption]:

        statement = (
            select(CouponRedemptionTable)
            .where(
                CouponRedemptionTable.coupon_id == coupon_id,
            )
            .order_by(
                CouponRedemptionTable.created_at.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def get_rows_by_coupon(
        self,
        *,
        coupon_id: int,
        offset: int,
        limit: int,
    ) -> tuple[list[CouponRedemption], int]:

        filters = [
            CouponRedemptionTable.coupon_id == coupon_id
        ]

        statement = (
            select(CouponRedemptionTable)
            .where(*filters)
            .order_by(
                CouponRedemptionTable.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        count_statement = (
            select(
                func.count(CouponRedemptionTable.id)
            )
            .where(*filters)
        )

        result = await self._db_session.execute(
            statement
        )

        count_result = await self._db_session.execute(
            count_statement
        )

        items = [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

        total_items = count_result.scalar_one()

        return items, total_items