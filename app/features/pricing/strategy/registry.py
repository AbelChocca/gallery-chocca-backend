from app.features.pricing.types import PricingRuleType
from app.features.pricing.strategy.base import BasePricingStrategy

from app.features.pricing.strategy.percentage import (
    PercentagePricingStrategy
)

from app.features.pricing.strategy.fixed import (
    FixedPricingStrategy
)

from app.features.pricing.strategy.final_price import (
    FinalPricePricingStrategy
)

PRICING_STRATEGIES: dict[str, BasePricingStrategy] = {
    PricingRuleType.PERCENTAGE: PercentagePricingStrategy(),
    PricingRuleType.FIXED: FixedPricingStrategy(),
    PricingRuleType.FINAL_PRICE: FinalPricePricingStrategy(),
}