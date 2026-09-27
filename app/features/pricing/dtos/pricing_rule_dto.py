from dataclasses import dataclass
from decimal import Decimal
from typing import TypeAlias

from app.features.pricing.types.pricing_rules_types import PricingRuleType

@dataclass(slots=True)
class PercentageRuleParameters:
    percentage: Decimal

@dataclass(slots=True)
class FixedAmountRuleParameters:
    amount: Decimal

@dataclass(slots=True)
class FixedPriceRuleParameters:
    price: Decimal

@dataclass(slots=True)
class BuyXGetYRuleParameters:
    buy_quantity: int

    free_quantity: int

@dataclass(slots=True)
class FreeItemRuleParameters:
    product_id: int

    quantity: int = 1

@dataclass(slots=True)
class FreeShippingRuleParameters:
    applies: bool = True

PricingRuleParameters: TypeAlias = (
    PercentageRuleParameters
    | FixedAmountRuleParameters
    | FixedPriceRuleParameters
    | BuyXGetYRuleParameters
    | FreeItemRuleParameters
    | FreeShippingRuleParameters
)

@dataclass(frozen=True, slots=True)
class PricingRuleSearchOptionDTO:
    id: int
    name: str
    description: str | None
    type: PricingRuleType
    parameters: dict