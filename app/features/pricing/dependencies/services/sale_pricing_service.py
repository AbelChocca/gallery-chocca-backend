from fastapi import Depends

from app.features.pricing.calculators.pricing_subtotal_calculator import (
    PricingSubtotalCalculator,
    get_pricing_subtotal_calculator
)
from app.features.pricing.calculators.pricing_item_calculator import (
    PricingItemCalculator,
    get_pricing_item_calculator
)
from app.features.pricing.resolvers.coupon_resolver import (
    CouponResolver,
    get_coupon_resolver,
)
from app.features.pricing.resolvers.promotion_audience_resolver import (
    PromotionAudienceResolver,
    get_audience_resolver,
)
from app.features.pricing.resolvers.promotion_condition_resolver import (
    PromotionConditionResolver,
    get_condition_resolver,
)
from app.features.pricing.resolvers.promotion_resolver import (
    PromotionResolver,
    get_promotion_resolver,
)
from app.features.pricing.resolvers.promotion_selection_resolver import (
    PromotionSelectionResolver,
    get_promotion_selection_resolver,
)
from app.features.pricing.services.sale_pricing import (
    SalePricingService,
)
from app.infra.db.uow.dependency import (
    get_uow,
)
from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)


def get_sale_pricing_service(
    uow: UnitOfWork = Depends(
        get_uow
    ),
    coupon_resolver: CouponResolver = Depends(
        get_coupon_resolver
    ),
    promotion_resolver: PromotionResolver = Depends(
        get_promotion_resolver
    ),
    promotion_audience_resolver: PromotionAudienceResolver = Depends(
        get_audience_resolver
    ),
    promotion_selection_resolver: PromotionSelectionResolver = Depends(
        get_promotion_selection_resolver
    ),
    promotion_condition_resolver: PromotionConditionResolver = Depends(
        get_condition_resolver
    ),
    pricing_item_calculator: PricingItemCalculator = Depends(
        get_pricing_item_calculator
    ),
    pricing_subtotal_calculator: PricingSubtotalCalculator = Depends(
        get_pricing_subtotal_calculator
    )
) -> SalePricingService:
    return SalePricingService(
        promotion_repository=uow.promotions,
        coupon_repository=uow.coupons,
        coupon_redemption_repository=uow.coupon_redemptions,
        coupon_resolver=coupon_resolver,
        promotion_resolver=promotion_resolver,
        promotion_audience_resolver=promotion_audience_resolver,
        promotion_selection_resolver=promotion_selection_resolver,
        promotion_condition_resolver=promotion_condition_resolver,
        pricing_item_calculator=pricing_item_calculator,
        pricing_subtotal_calculator=pricing_subtotal_calculator
    )