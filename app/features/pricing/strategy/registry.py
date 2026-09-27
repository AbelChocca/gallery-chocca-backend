from app.features.pricing.types.pricing_rules_types import PricingRuleType

from app.features.pricing.strategy.base import BasePricingStrategy
from app.features.pricing.strategy.percentage import (
    PercentagePricingStrategy,
)
from app.features.pricing.strategy.fixed_amount import (
    FixedAmountPricingStrategy,
)
from app.features.pricing.strategy.fixed_price import (
    FixedPricePricingStrategy,
)
from app.features.pricing.strategy.buy_x_get_y import (
    BuyXGetYPricingStrategy,
)
from app.features.pricing.strategy.free_item import (
    FreeItemPricingStrategy,
)
from app.features.pricing.strategy.free_shipping import (
    FreeShippingPricingStrategy,
)


PRICING_STRATEGIES: dict[str, BasePricingStrategy] = {
    PricingRuleType.PERCENTAGE: PercentagePricingStrategy(),
    PricingRuleType.FIXED_AMOUNT: FixedAmountPricingStrategy(),
    PricingRuleType.FIXED_PRICE: FixedPricePricingStrategy(),
    PricingRuleType.BUY_X_GET_Y: BuyXGetYPricingStrategy(),
    PricingRuleType.FREE_ITEM: FreeItemPricingStrategy(),
    PricingRuleType.FREE_SHIPPING: FreeShippingPricingStrategy(),
}