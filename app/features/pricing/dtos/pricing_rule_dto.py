from dataclasses import dataclass
from decimal import Decimal
from typing import TypeAlias

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
    variant_size_id: int

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