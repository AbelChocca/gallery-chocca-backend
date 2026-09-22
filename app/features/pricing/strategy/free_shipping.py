from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)

from app.features.pricing.dtos.pricing_rule_dto import (
    FreeShippingRuleParameters,
)

class FreeShippingPricingStrategy(BasePricingStrategy[FreeShippingRuleParameters]):
    """
    Parameters:

    {}

    No parameters are required.

    The promotion sets the current shipping cost to zero.
    """

    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: FreeShippingRuleParameters,
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        return PricingStrategyResult(
            unit_price=current_price,
            discount_amount=Decimal("0.00"),
            shipping_cost=Decimal("0.00"),
        )

    def validate(
        self,
        parameters: FreeShippingRuleParameters,
    ) -> None:
        pass