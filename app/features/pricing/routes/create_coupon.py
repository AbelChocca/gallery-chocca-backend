from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.services.coupon import (
    CouponService,
)
from app.features.pricing.schemas.coupon_schema import CreateCouponSchema, CouponResponseSchema

from app.features.pricing.dependencies.services.coupon import (
    get_coupon_service,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)


@router.post(
    "/coupons",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
        )
    ],
)
async def create_coupon(
    schema: CreateCouponSchema,
    coupon_service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
) -> CouponResponseSchema:

    coupon = await coupon_service.create(
        promotion_id=schema.promotion_id,
        code=schema.code,
        is_active=schema.is_active,
        starts_at=schema.starts_at,
        ends_at=schema.ends_at,
        max_redemptions=schema.max_redemptions,
        max_redemptions_per_customer=(
            schema.max_redemptions_per_customer
        ),
    )

    return CouponResponseSchema.model_validate(
        coupon
    )