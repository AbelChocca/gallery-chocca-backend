from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any
from app.features.pricing.types.pricing_rules_types import PricingStrategyResult


class BasePricingStrategy(ABC):
    @abstractmethod
    def apply(
        self,
        *,
        current_price: Decimal,
        quantity: int,
        parameters: dict[str, Any],
        shipping_cost: Decimal,
    ) -> PricingStrategyResult:
        pass

    @abstractmethod
    def validate(
        self,
        parameters: dict[str, Any],
    ) -> None:
        pass