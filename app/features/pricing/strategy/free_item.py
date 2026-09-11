from decimal import Decimal
from typing import Any

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)


class FreeItemPricingStrategy(BasePricingStrategy):
    """
    Parameters:

    {
        "quantity": 1
    }

    `quantity`:
        Cantidad de unidades gratuitas.

    Ejemplo:
        quantity=1
        -> Una unidad del producto es gratuita.
    """

    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: dict[str, Any],
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        free_quantity = min(
            int(parameters["quantity"]),
            quantity,
        )

        discount_amount = current_price * free_quantity

        if quantity == 0:
            unit_price = current_price
        else:
            final_total = (
                current_price * quantity
            ) - discount_amount

            unit_price = final_total / quantity

        return PricingStrategyResult(
            unit_price=unit_price,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
        )

    def validate(
        self,
        parameters: dict[str, Any],
    ) -> None:
        if "quantity" not in parameters:
            raise ValueError(
                "Free item pricing rule requires 'quantity'"
            )

        quantity = int(parameters["quantity"])

        if quantity <= 0:
            raise ValueError(
                "Free item quantity must be greater than 0"
            )