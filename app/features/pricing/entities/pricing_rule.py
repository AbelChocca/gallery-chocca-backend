from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.features.pricing.types.pricing_rules_types import (
    PricingRuleType,
)
from app.features.pricing.strategy.registry import (
    PRICING_STRATEGIES,
)


@dataclass
class PricingRule:
    id: int | None = None

    name: str = ""
    description: str | None = None

    type: PricingRuleType = PricingRuleType.PERCENTAGE

    parameters: dict[str, Any] = field(
        default_factory=dict,
    )

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self.validate()

    @property
    def strategy(self):
        return PRICING_STRATEGIES[self.type]

    def validate(self) -> None:
        self.strategy.validate(
            self.parameters,
        )

    def apply(
        self,
        *,
        current_price,
        quantity: int = 1,
        shipping_cost,
    ):
        return self.strategy.apply(
            current_price=current_price,
            quantity=quantity,
            parameters=self.parameters,
            shipping_cost=shipping_cost,
        )