from app.features.pricing.entities.coupon import Coupon
from app.features.pricing.models.coupon import CouponTable
from app.infra.db.mappers.base_mapper import BaseMapper


class CouponMapper(
    BaseMapper[Coupon, CouponTable]
):

    @staticmethod
    def to_db_model(
        entity: Coupon,
        existing_model: CouponTable | None = None,
    ) -> CouponTable:
        model = existing_model or CouponTable()

        model.promotion_id = entity.promotion_id
        model.code = entity.code
        model.is_active = entity.is_active
        model.starts_at = entity.starts_at
        model.ends_at = entity.ends_at
        model.max_redemptions = entity.max_redemptions
        model.max_redemptions_per_customer = (
            entity.max_redemptions_per_customer
        )
        model.used_count = entity.used_count

        return model

    @staticmethod
    def to_entity(
        model: CouponTable,
    ) -> Coupon:
        return Coupon(
            id=model.id,
            promotion_id=model.promotion_id,
            code=model.code,
            is_active=model.is_active,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            max_redemptions=model.max_redemptions,
            max_redemptions_per_customer=(
                model.max_redemptions_per_customer
            ),
            used_count=model.used_count,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )