from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy,
)

from app.features.pricing.dtos.pricing_rule_dto import (
    PercentageRuleParameters,
)

from app.features.pricing.types.pricing_rules_types import (
    PricingStrategyResult,
)
from app.core.exceptions import ValidationError


class PercentagePricingStrategy(
    BasePricingStrategy[PercentageRuleParameters]
):
    """
    Parameters:

    {
        "percentage": "20.00"
    }

    `value`:
        Porcentaje de descuento a aplicar.
        Ejemplo: "20.00" = 20% de descuento.
    """

    def validate(
        self,
        parameters: PercentageRuleParameters,
    ) -> None:
        if parameters.percentage <= 0:
            raise ValidationError(
                "El porcentaje debe ser mayor que cero.",
                {
                    "strategy": "PercentagePricingStrategy",
                    "event": "validate",
                    "percentage": str(
                        parameters.percentage
                    ),
                },
            )

        if parameters.percentage > 100:
            raise ValidationError(
                "El porcentaje no puede ser mayor a 100.",
                {
                    "strategy": "PercentagePricingStrategy",
                    "event": "validate",
                    "percentage": str(
                        parameters.percentage
                    ),
                },
            )

    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: PercentageRuleParameters,
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:

        discount_per_unit = (
            current_price
            * parameters.percentage
            / Decimal("100")
        )

        final_price = (
            current_price
            - discount_per_unit
        )

        return PricingStrategyResult(
            unit_price=final_price,
            shipping_cost=shipping_cost,
            discount_amount=(
                discount_per_unit
                * quantity
            ),
        )