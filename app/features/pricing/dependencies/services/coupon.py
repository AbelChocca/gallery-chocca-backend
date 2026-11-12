from fastapi import Depends

from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)
from app.infra.db.uow.dependency import (
    get_uow,
)

from app.features.pricing.services.coupon import (
    CouponService,
)
from app.features.pricing.resolvers.coupon_resolver import CouponResolver, get_coupon_resolver
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service



def get_coupon_service(
    uow: UnitOfWork = Depends(get_uow),
    coupon_resolver: CouponResolver = Depends(get_coupon_resolver),
    pagination_service: 
        PaginationService =
        Depends(get_pagination_service),
) -> CouponService:

    return CouponService(
        coupon_repository=uow.coupons,
        coupon_redemption_repository=(
            uow.coupon_redemptions
        ),
        coupon_resolver=coupon_resolver,
        pagination_service=pagination_service,
    )