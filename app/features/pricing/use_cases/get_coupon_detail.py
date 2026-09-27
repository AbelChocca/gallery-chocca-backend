from app.features.pricing.dtos.cuopon_dto import (
    CouponDetailDTO,
    CouponPromotionDTO,
)

from app.features.pricing.services.coupon import (
    CouponService,
)
from app.features.pricing.services.promotion import (
    PromotionService,
)


class GetCouponDetailUseCase:

    def __init__(
        self,
        *,
        coupon_service: CouponService,
        promotion_service: PromotionService,
    ) -> None:
        self._coupon_service = coupon_service
        self._promotion_service = promotion_service

    async def execute(
        self,
        *,
        coupon_id: int,
    ) -> CouponDetailDTO:

        coupon = await self._coupon_service.get_by_id(
            coupon_id=coupon_id,
        )

        promotion = await self._promotion_service.get_by_id(
            promotion_id=coupon.promotion_id,
        )

        promotion_dto = CouponPromotionDTO(
            id=promotion.id,
            name=promotion.name,
            description=promotion.description,
            sales_channel=promotion.sales_channel,
            stacking_mode=promotion.stacking_mode,
            priority=promotion.priority,
            is_active=promotion.is_active,
        )

        return CouponDetailDTO(
            id=coupon.id,
            promotion_id=coupon.promotion_id,
            code=coupon.code,
            is_active=coupon.is_active,
            starts_at=coupon.starts_at,
            ends_at=coupon.ends_at,
            max_redemptions=coupon.max_redemptions,
            max_redemptions_per_customer=(
                coupon.max_redemptions_per_customer
            ),
            used_count=coupon.used_count,
            promotion=promotion_dto,
            created_at=coupon.created_at,
            updated_at=coupon.updated_at,
        )