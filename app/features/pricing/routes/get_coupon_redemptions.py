from typing import Annotated

from fastapi import (
    Depends,
    Path,
    Query,
    status,
)

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.schemas.coupon_schema import (
    CouponRedemptionResponseSchema,
)

from app.features.pricing.services.coupon import (
    CouponService,
)

from app.features.pricing.dependencies.services.coupon import (
    get_coupon_service,
)

from app.shared.pagination.schema import (
    PaginatedResponseSchema,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)


@router.get(
    "/coupons/{coupon_id}/redemptions",
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_READ,
        )
    ],
)
async def get_coupon_redemptions(
    coupon_id: Annotated[
        int,
        Path(gt=0),
    ],
    service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
    page: Annotated[
        int,
        Query(ge=1),
    ] = 1,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
        ),
    ] = 20,
) -> PaginatedResponseSchema[
    CouponRedemptionResponseSchema
]:

    result = await service.get_redemption_rows(
        coupon_id=coupon_id,
        page=page,
        limit=limit,
    )

    return PaginatedResponseSchema[
        CouponRedemptionResponseSchema
    ].model_validate(result)