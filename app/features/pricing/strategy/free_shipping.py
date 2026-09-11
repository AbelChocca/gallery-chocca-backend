from decimal import Decimal
from typing import Any

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)


class FreeShippingPricingStrategy(BasePricingStrategy):
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
        parameters: dict[str, Any],
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        return PricingStrategyResult(
            unit_price=current_price,
            discount_amount=Decimal("0.00"),
            shipping_cost=Decimal("0.00"),
        )

    def validate(
        self,
        parameters: dict[str, Any],
    ) -> None:
        pass