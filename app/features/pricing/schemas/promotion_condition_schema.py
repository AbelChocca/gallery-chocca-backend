from decimal import Decimal
from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict
from app.features.sales.types.payment import PaymentMethod
from app.features.pricing.types.promotion_types import PromotionConditionType

class MinimumOrderAmountConditionParametersSchema(BaseModel):
    minimum_amount: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


class MinimumProductQuantityConditionParametersSchema(BaseModel):
    minimum_quantity: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class PaymentMethodConditionParametersSchema(BaseModel):
    payment_method: PaymentMethod

    model_config = ConfigDict(
        from_attributes=True,
    )


PromotionConditionParametersSchema = Union[
    MinimumOrderAmountConditionParametersSchema,
    MinimumProductQuantityConditionParametersSchema,
    PaymentMethodConditionParametersSchema,
]

class CreatePromotionConditionSchema(BaseModel):
    condition_type: PromotionConditionType
    parameters: PromotionConditionParametersSchema
    description: str | None = None

class PromotionConditionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    promotion_id: int
    condition_type: PromotionConditionType
    parameters: PromotionConditionParametersSchema
    description: str | None
    created_at: datetime | None

class ReplacePromotionConditionsSchema(BaseModel):
    conditions: list[CreatePromotionConditionSchema]