from decimal import Decimal
from typing import Any

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)


class BuyXGetYPricingStrategy(BasePricingStrategy):
    """
    Parameters:

    {
        "buy_quantity": 2,
        "free_quantity": 1
    }

    `buy_quantity`:
        Cantidad de unidades que el cliente debe pagar.

    `free_quantity`:
        Cantidad de unidades gratuitas.

    Ejemplo:
        buy_quantity=2
        free_quantity=1

        -> Lleva 3 unidades pagando solamente 2.
    """

    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: dict[str, Any],
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        buy_quantity = int(parameters["buy_quantity"])
        free_quantity = int(parameters["free_quantity"])

        group_size = buy_quantity + free_quantity

        free_units = (
            quantity // group_size
        ) * free_quantity

        paid_units = quantity - free_units

        if quantity == 0:
            return PricingStrategyResult(
                unit_price=current_price,
                discount_amount=Decimal("0.00"),
                shipping_cost=shipping_cost,
            )

        final_total = current_price * paid_units

        unit_price = final_total / quantity

        discount_amount = (
            current_price * free_units
        )

        return PricingStrategyResult(
            unit_price=unit_price,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
        )

    def validate(
        self,
        parameters: dict[str, Any],
    ) -> None:
        required = {
            "buy_quantity",
            "free_quantity",
        }

        missing = required - parameters.keys()

        if missing:
            raise ValueError(
                f"Buy X Get Y pricing rule requires: {missing}"
            )

        buy_quantity = int(parameters["buy_quantity"])
        free_quantity = int(parameters["free_quantity"])

        if buy_quantity <= 0:
            raise ValueError(
                "buy_quantity must be greater than 0"
            )

        if free_quantity <= 0:
            raise ValueError(
                "free_quantity must be greater than 0"
            )