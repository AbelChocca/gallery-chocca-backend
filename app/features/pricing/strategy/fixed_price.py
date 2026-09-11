from decimal import Decimal
from typing import Any

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)


class FixedPricePricingStrategy(BasePricingStrategy):
    """
    Parameters:

    {
        "value": "79.90"
    }

    `value`:
        Precio final fijo por unidad.
        Ejemplo: "79.90" = el producto tendrá un precio de S/79.90.
    """

    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: dict[str, Any],
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        unit_price = Decimal(str(parameters["value"]))

        discount = max(
            Decimal("0.00"),
            current_price - unit_price,
        )

        return PricingStrategyResult(
            unit_price=unit_price,
            discount_amount=discount * quantity,
            shipping_cost=shipping_cost,
        )

    def validate(
        self,
        parameters: dict[str, Any],
    ) -> None:
        if "value" not in parameters:
            raise ValueError(
                "Fixed price pricing rule requires 'value'"
            )

        value = Decimal(str(parameters["value"]))

        if value < Decimal("0"):
            raise ValueError(
                "Fixed price value cannot be negative"
            )