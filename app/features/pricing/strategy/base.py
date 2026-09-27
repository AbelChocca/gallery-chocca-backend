from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Generic, TypeVar

from app.features.pricing.dtos.pricing_rule_dto import (
    PricingRuleParameters,
)

from app.features.pricing.types.pricing_rules_types import (
    PricingStrategyResult,
)


P = TypeVar(
    "P",
    bound=PricingRuleParameters,
)


class BasePricingStrategy(
    ABC,
    Generic[P],
):

    @abstractmethod
    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: P,
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        pass

    @abstractmethod
    def validate(
        self,
        parameters: P,
    ) -> None:
        pass