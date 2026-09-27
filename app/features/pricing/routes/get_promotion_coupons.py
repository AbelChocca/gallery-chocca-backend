from typing import Annotated

from fastapi import (
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.schemas.coupon_schema import (
    CouponResponseSchema,

)

from app.features.pricing.services.coupon import (
    CouponService,
)

from app.features.pricing.dependencies.services.coupon import (
    get_coupon_service,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)

@router.get(
    "/promotions/{promotion_id}/coupons",
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_READ,
        )
    ],
)
async def get_promotion_coupons(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    coupon_service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
) -> list[CouponResponseSchema]:

    coupons = await coupon_service.get_by_promotion(
        promotion_id=promotion_id,
    )

    return [
        CouponResponseSchema.model_validate(
            coupon
        )
        for coupon in coupons
    ]