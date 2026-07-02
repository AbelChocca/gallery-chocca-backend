from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy
)
from app.core.exceptions import InvalidOperation

class FixedPricingStrategy(BasePricingStrategy):
    def validate(
        self,
        value
    ) -> None:

        if value <= 0:
            raise InvalidOperation(
                "Fixed discount must be greater than 0"
            )

    def apply(
        self,
        *,
        current_price: Decimal,
        value
    ) -> Decimal:
        self.validate(value)

        final_price = current_price - value

        if final_price < 0:
            return Decimal("0")

        return final_price