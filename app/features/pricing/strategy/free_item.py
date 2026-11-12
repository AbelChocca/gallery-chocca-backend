from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)

from app.features.pricing.dtos.pricing_rule_dto import (
    FreeItemRuleParameters,
)

from app.core.exceptions import ValidationError


class FreeItemPricingStrategy(BasePricingStrategy[FreeItemRuleParameters]):
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
        parameters: FreeItemRuleParameters,
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        free_quantity = min(
            parameters.quantity,
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
        parameters: FreeItemRuleParameters,
    ) -> None:
        if not parameters.quantity:
            raise ValidationError(
                "Free item pricing rule requires 'quantity'"
            )

        if parameters.quantity <= 0:
            raise ValidationError(
                "Free item quantity must be greater than 0"
            )