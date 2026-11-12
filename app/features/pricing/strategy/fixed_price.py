from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
)

from app.features.pricing.dtos.pricing_rule_dto import (
    FixedPriceRuleParameters,
)

from app.features.pricing.types.pricing_rules_types import (
    PricingStrategyResult,
)
from app.core.exceptions import ValidationError


class FixedPricePricingStrategy(BasePricingStrategy[FixedPriceRuleParameters]):
    """
    Parameters:

    {
        "price": "79.90"
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
        parameters: FixedPriceRuleParameters,
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        unit_price = parameters.price

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
        parameters: FixedPriceRuleParameters,
    ) -> None:
        if not parameters.price:
            raise ValidationError(
                "Fixed price pricing rule requires 'price'"
            )

        value = parameters.price

        if value < Decimal("0"):
            raise ValidationError(
                "Fixed price value cannot be negative"
            )