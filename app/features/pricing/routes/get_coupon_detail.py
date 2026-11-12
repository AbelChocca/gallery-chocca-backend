from typing import Annotated

from fastapi import (
    Depends,
    Path,
    status,
)
from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.use_cases.get_coupon_detail import (
    GetCouponDetailUseCase,
)

from app.features.pricing.dependencies.use_cases.get_coupon_detail import (
    get_coupon_detail_use_case,
)

from app.features.pricing.schemas.coupon_schema import (
    CouponDetailResponseSchema,
)
from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)



@router.get(
    "/coupons/{coupon_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_READ,
        )
    ],
)
async def get_coupon_detail(
    coupon_id: Annotated[
        int,
        Path(gt=0),
    ],
    use_case: Annotated[
        GetCouponDetailUseCase,
        Depends(get_coupon_detail_use_case),
    ],
) -> CouponDetailResponseSchema:

    result = await use_case.execute(
        coupon_id=coupon_id,
    )

    return CouponDetailResponseSchema.model_validate(
        result
    )