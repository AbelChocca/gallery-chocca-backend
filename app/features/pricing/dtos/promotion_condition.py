from dataclasses import dataclass
from decimal import Decimal
from typing import TypeAlias

from app.features.pricing.types.promotion_types import PromotionConditionType
from app.features.sales.types.payment import PaymentMethod

@dataclass(slots=True)
class MinimumOrderAmountConditionParameters:
    minimum_amount: Decimal

@dataclass(slots=True)
class PaymentMethodConditionParameters:
    payment_method: PaymentMethod

@dataclass(slots=True)
class MinimumProductQuantityConditionParameters:
    minimum_quantity: int

PromotionConditionParameters: TypeAlias = (
    MinimumOrderAmountConditionParameters
    | MinimumProductQuantityConditionParameters
    | PaymentMethodConditionParameters
)

@dataclass(slots=True)
class AppliedPromotionConditionDTO:
    type: PromotionConditionType

    parameters: PromotionConditionParameters