from pydantic import BaseModel, ConfigDict
from typing import Union
from datetime import datetime
from decimal import Decimal
from app.features.pricing.types.pricing_rules_types import PricingRuleType

class PercentageRuleParametersSchema(BaseModel):
    percentage: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


class FixedAmountRuleParametersSchema(BaseModel):
    amount: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


class FixedPriceRuleParametersSchema(BaseModel):
    price: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


class BuyXGetYRuleParametersSchema(BaseModel):
    buy_quantity: int
    free_quantity: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class FreeItemRuleParametersSchema(BaseModel):
    product_id: int
    quantity: int = 1

    model_config = ConfigDict(
        from_attributes=True,
    )


class FreeShippingRuleParametersSchema(BaseModel):
    applies: bool = True

    model_config = ConfigDict(
        from_attributes=True,
    )


PricingRuleParametersSchema = Union[
    PercentageRuleParametersSchema,
    FixedAmountRuleParametersSchema,
    FixedPriceRuleParametersSchema,
    BuyXGetYRuleParametersSchema,
    FreeItemRuleParametersSchema,
    FreeShippingRuleParametersSchema,
]

class ExistingPromotionPricingRuleSchema(BaseModel):

    pricing_rule_id: int
    execution_order: int = 0


class NewPromotionPricingRuleSchema(BaseModel):

    name: str
    description: str | None = None
    type: PricingRuleType
    parameters: PricingRuleParametersSchema

    execution_order: int = 0


PromotionPricingRuleInputSchema = Union[
    ExistingPromotionPricingRuleSchema
    | NewPromotionPricingRuleSchema,
]

class PricingRuleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    type: PricingRuleType
    parameters: PricingRuleParametersSchema
    created_at: datetime | None
    updated_at: datetime | None

class ReplacePromotionPricingRulesSchema(BaseModel):
    pricing_rules: list[
        ExistingPromotionPricingRuleSchema
    ]

class PricingRuleSearchOptionResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    description: str | None
    type: PricingRuleType
    parameters: PricingRuleParametersSchema