from typing import Annotated

from fastapi import Depends

from app.features.pricing.use_cases.get_coupon_detail import (
    GetCouponDetailUseCase,
)

from app.features.pricing.services.coupon import (
    CouponService,
)
from app.features.pricing.services.promotion import (
    PromotionService,
)

from app.features.pricing.dependencies.services.coupon import (
    get_coupon_service,
)
from app.features.pricing.dependencies.services.promotion import get_promotion_service


def get_coupon_detail_use_case(
    coupon_service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
    promotion_service: Annotated[
        PromotionService,
        Depends(get_promotion_service),
    ],
) -> GetCouponDetailUseCase:

    return GetCouponDetailUseCase(
        coupon_service=coupon_service,
        promotion_service=promotion_service,
    )