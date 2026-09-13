import pytest_asyncio

from app.features.pricing.calculators.pricing_calculator import (
    PricingCalculator,
)
from app.features.pricing.mappers.coupon_mapper import CouponMapper
from app.features.pricing.mappers.coupon_redemption_mapper import (
    CouponRedemptionMapper,
)
from app.features.pricing.mappers.promotion_mapper import PromotionMapper
from app.features.pricing.models.coupon import CouponTable
from app.features.pricing.models.coupon_redemption import (
    CouponRedemptionTable,
)
from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.repositories.coupon_redemption_repository import (
    CouponRedemptionRepository,
)
from app.features.pricing.repositories.coupon_repsitory import (
    CouponRepository,
)
from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
)
from app.features.pricing.resolvers.coupon_resolver import (
    CouponResolver,
)
from app.features.pricing.resolvers.promotion_audience_resolver import (
    PromotionAudienceResolver,
)
from app.features.pricing.resolvers.promotion_condition_resolver import (
    PromotionConditionResolver,
)
from app.features.pricing.services.sale_pricing import (
    SalePricingService,
)


@pytest_asyncio.fixture
def sale_pricing_service(db_session):
    promotion_repository = PromotionRepository(
        db_session=db_session,
        base_mapper=PromotionMapper,
        base_model=PromotionTable,
    )

    coupon_repository = CouponRepository(
        db_session=db_session,
        base_mapper=CouponMapper,
        base_model=CouponTable,
    )

    coupon_redemption_repository = CouponRedemptionRepository(
        db_session=db_session,
        base_mapper=CouponRedemptionMapper,
        base_model=CouponRedemptionTable,
    )

    return SalePricingService(
        promotion_repository=promotion_repository,
        coupon_repository=coupon_repository,
        coupon_redemption_repository=coupon_redemption_repository,
        pricing_calculator=PricingCalculator(),
        coupon_resolver=CouponResolver(),
        promotion_audience_resolver=PromotionAudienceResolver(),
        promotion_condition_resolver=PromotionConditionResolver(),
    )