from typing import Annotated

from fastapi import (
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import (
    router,
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


@router.post(
    "/coupons/{coupon_id}/toggle_status",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
        )
    ],
)
async def toggle_coupon_status(
    coupon_id: Annotated[
        int,
        Path(gt=0),
    ],
    coupon_service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
) -> None:

    await coupon_service.toggle_status(
        coupon_id=coupon_id,
    )