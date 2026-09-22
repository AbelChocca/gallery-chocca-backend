from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
    PricingStrategyResult,
)

from app.features.pricing.dtos.pricing_rule_dto import (
    FixedAmountRuleParameters,
)
from app.core.exceptions import ValidationError

class FixedAmountPricingStrategy(
    BasePricingStrategy[FixedAmountRuleParameters]
):
    """
    Parameters:

    {
        "amount": "15.00"
    }

    `amount`:
        Monto fijo de descuento por unidad.
        Ejemplo: "15.00" = S/15.00 de descuento por unidad.
    """

    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: FixedAmountRuleParameters,
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        value = parameters.amount

        discount = min(value, current_price)
        unit_price = current_price - discount

        return PricingStrategyResult(
            unit_price=unit_price,
            discount_amount=discount * quantity,
            shipping_cost=shipping_cost,
        )

    def validate(
        self,
        parameters: FixedAmountRuleParameters,
    ) -> None:
        if not parameters.amount:
            raise ValidationError(
                "Fixed amount pricing rule requires 'amount'"
            )

        value = parameters.amount

        if value < Decimal("0"):
            raise ValidationError(
                "Fixed amount value cannot be negative"
            )