from datetime import datetime
from typing import Any

from app.features.pricing.types.types import PricingRuleType
from app.features.pricing.strategy.registry import PRICING_STRATEGIES


class PricingRule:

    def __init__(
        self,
        id: int | None = None,
        name: str = "",
        description: str | None = None,
        type: PricingRuleType = PricingRuleType.PERCENTAGE,
        parameters: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.parameters = parameters or {}
        self.created_at = created_at
        self.updated_at = updated_at

        self.validate()

    @property
    def strategy(self):
        return PRICING_STRATEGIES[self.type]

    def validate(self) -> None:
        self.strategy.validate(
            self.parameters
        )

    def apply(
        self,
        *,
        current_price,
        quantity: int = 1,
    ):
        return self.strategy.apply(
            current_price=current_price,
            quantity=quantity,
            parameters=self.parameters,
        )