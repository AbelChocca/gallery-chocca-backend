from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy
)
from app.core.exceptions import InvalidOperation

class FinalPricePricingStrategy(BasePricingStrategy):
    def validate(
        self,
        value: Decimal
    ) -> None:

        if value < 0:
            raise InvalidOperation(
                "Final price cannot be negative"
            )

    def apply(
        self,
        *,
        current_price: Decimal,
        value
    ) -> Decimal:
        if value < 0:
            return Decimal("0")

        return value