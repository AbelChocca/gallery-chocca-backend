from decimal import Decimal
from typing import Any

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)


class FixedAmountPricingStrategy(BasePricingStrategy):
    """
    Parameters:

    {
        "value": "15.00"
    }

    `value`:
        Monto fijo de descuento por unidad.
        Ejemplo: "15.00" = S/15.00 de descuento por unidad.
    """

    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: dict[str, Any],
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        value = Decimal(str(parameters["value"]))

        discount = min(value, current_price)
        unit_price = current_price - discount

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
                "Fixed amount pricing rule requires 'value'"
            )

        value = Decimal(str(parameters["value"]))

        if value < Decimal("0"):
            raise ValueError(
                "Fixed amount value cannot be negative"
            )