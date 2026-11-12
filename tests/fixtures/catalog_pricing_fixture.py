import pytest_asyncio

from app.features.pricing.services.catalog_pricing import CatalogPricingService
from app.features.pricing.resolvers.promotion_selection_resolver import PromotionSelectionResolver
from app.features.pricing.calculators.pricing_item_calculator import PricingItemCalculator
from app.features.pricing.mappers.promotion_mapper import PromotionMapper
from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
)
from app.features.pricing.resolvers.promotion_audience_resolver import (
    PromotionAudienceResolver,
)
from app.features.pricing.resolvers.promotion_resolver import PromotionResolver

@pytest_asyncio.fixture
def catalog_pricing_service(db_session):

    promotion_repository = PromotionRepository(
        db_session=db_session,
        base_mapper=PromotionMapper,
        base_model=PromotionTable,
    )

    return CatalogPricingService(
        promotion_repository=promotion_repository,
        promotion_resolver=PromotionResolver(),
        promotion_selection_resolver=PromotionSelectionResolver(),
        promotion_audience_resolver=PromotionAudienceResolver(),
        pricing_item_calculator=PricingItemCalculator(),
    )