from fastapi import Depends

from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)
from app.infra.db.uow.dependency import (
    get_uow,
)

from app.features.pricing.services.catalog_pricing import (
    CatalogPricingService,
)

from app.features.pricing.resolvers.promotion_resolver import (
    get_promotion_resolver,
    PromotionResolver
)
from app.features.pricing.resolvers.promotion_audience_resolver import (
    get_audience_resolver,
    PromotionAudienceResolver
)
from app.features.pricing.calculators.pricing_item_calculator import (
    get_pricing_item_calculator,
    PricingItemCalculator
)
from app.features.pricing.resolvers.promotion_selection_resolver import (
    get_promotion_selection_resolver,
    PromotionSelectionResolver
)


def get_catalog_pricing_service(
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
    pricing_item_calculator: PricingItemCalculator = Depends(
        get_pricing_item_calculator
    ),
) -> CatalogPricingService:

    return CatalogPricingService(
        promotion_repository=uow.promotions,
        promotion_resolver=promotion_resolver,
        promotion_selection_resolver=promotion_selection_resolver,
        promotion_audience_resolver=promotion_audience_resolver,
        pricing_item_calculator=pricing_item_calculator,
    )