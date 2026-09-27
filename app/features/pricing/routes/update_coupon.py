from typing import Annotated

from fastapi import (
    Depends,
    Path,
    status,
    Body
)

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.schemas.coupon_schema import (
    UpdateCouponSchema,
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


@router.patch(
    "/coupons/{coupon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
        )
    ],
)
async def update_coupon(
    coupon_id: Annotated[
        int,
        Path(gt=0),
    ],
    schema: Annotated[
        UpdateCouponSchema,
        Body(),
    ],
    coupon_service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
) -> None:

    changes = schema.model_dump(
        exclude_unset=True,
    )

    await coupon_service.update(
        coupon_id=coupon_id,
        changes=changes,
    )