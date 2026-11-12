from fastapi import Depends

from app.features.pricing.calculators.pricing_item_calculator import (
    PricingItemCalculator, get_pricing_item_calculator
)
from app.features.pricing.resolvers.promotion_audience_resolver import get_audience_resolver
from app.features.pricing.resolvers.promotion_condition_resolver import get_condition_resolver
from app.features.pricing.resolvers.promotion_resolver import get_promotion_resolver
from app.features.pricing.resolvers.promotion_selection_resolver import get_promotion_selection_resolver
from app.features.pricing.calculators.pricing_subtotal_calculator import PricingSubtotalCalculator, get_pricing_subtotal_calculator
from app.features.pricing.resolvers.promotion_audience_resolver import (
    PromotionAudienceResolver,
)
from app.features.pricing.resolvers.promotion_condition_resolver import (
    PromotionConditionResolver,
)
from app.features.pricing.resolvers.promotion_resolver import (
    PromotionResolver,
)
from app.features.pricing.resolvers.promotion_selection_resolver import (
    PromotionSelectionResolver,
)
from app.features.pricing.services.cart_pricing import (
    CartPricingService,
)
from app.infra.db.uow.dependency import (
    get_uow,
)
from app.infra.db.uow.unit_of_work import UnitOfWork


def get_cart_pricing_service(
    uow: UnitOfWork = Depends(get_uow),
    promotion_resolver: PromotionResolver = Depends(
        get_promotion_resolver
    ),
    promotion_selection_resolver: PromotionSelectionResolver = Depends(
        get_promotion_selection_resolver
    ),
    promotion_audience_resolver: PromotionAudienceResolver = Depends(
        get_audience_resolver
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
) -> CartPricingService:
    return CartPricingService(
        promotion_repository=uow.promotions,
        promotion_resolver=promotion_resolver,
        promotion_selection_resolver=(
            promotion_selection_resolver
        ),
        promotion_audience_resolver=(
            promotion_audience_resolver
        ),
        promotion_condition_resolver=(
            promotion_condition_resolver
        ),
        pricing_item_calculator=(
            pricing_item_calculator
        ),
        pricing_subtotal_calculator=pricing_subtotal_calculator
    )