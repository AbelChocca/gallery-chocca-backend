from decimal import Decimal

from app.features.pricing.strategy.base import (
    BasePricingStrategy
)
from app.core.exceptions import InvalidOperation

class PercentagePricingStrategy(BasePricingStrategy):

    def validate(
        self,
        value
    ) -> None:

        if value <= 0:
            raise InvalidOperation(
                "Percentage discount must be greater than 0"
            )

        if value > 100:
            raise InvalidOperation(
                "Percentage discount cannot exceed 100"
            )

    def apply(
        self,
        *,
        current_price: Decimal,
        value: Decimal
    ) -> Decimal:
        self.validate(value)

        discount = (
            current_price * (value / Decimal("100"))
        )

        return current_price - discount