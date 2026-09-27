from app.features.pricing.entities.coupon_redemption import CouponRedemption
from app.features.pricing.models.coupon_redemption import (
    CouponRedemptionTable,
)
from app.infra.db.mappers.base_mapper import BaseMapper


class CouponRedemptionMapper(
    BaseMapper[CouponRedemption, CouponRedemptionTable]
):

    @staticmethod
    def to_db_model(
        entity: CouponRedemption,
        existing_model: CouponRedemptionTable | None = None,
    ) -> CouponRedemptionTable:
        model = existing_model or CouponRedemptionTable()

        model.coupon_id = entity.coupon_id
        model.customer_id = entity.customer_id

        return model

    @staticmethod
    def to_entity(
        model: CouponRedemptionTable,
    ) -> CouponRedemption:
        return CouponRedemption(
            id=model.id,
            coupon_id=model.coupon_id,
            customer_id=model.customer_id,
            created_at=model.created_at,
        )