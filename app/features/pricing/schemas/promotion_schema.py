from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.features.pricing.types.promotion_types import (
    PromotionStackingMode,
    PromotionApplicationScope
)

from app.features.pricing.schemas.pricing_rule_schema import PromotionPricingRuleInputSchema, PricingRuleResponseSchema
from app.features.pricing.schemas.promotion_audience_schema import PromotionAudienceResponseSchema, CreatePromotionAudienceSchema
from app.features.pricing.schemas.promotion_condition_schema import PromotionConditionResponseSchema, CreatePromotionConditionSchema
from app.features.pricing.schemas.promotion_target_schema import PromotionTargetResponseSchema, CreatePromotionTargetSchema
from app.features.pricing.schemas.coupon_schema import CouponResponseSchema

from app.features.sales.types.sale import (
    SaleChannel,
)


class CreatePromotionSchema(BaseModel):
    name: str
    description: str | None = None

    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    application_scope: PromotionApplicationScope

    priority: int = 0

    starts_at: datetime | None = None
    ends_at: datetime | None = None

    is_active: bool = True

    pricing_rules: list[
        PromotionPricingRuleInputSchema
    ] = Field(default_factory=list)

    audiences: list[CreatePromotionAudienceSchema] = Field(
        default_factory=list
    )

    targets: list[CreatePromotionTargetSchema] = Field(
        default_factory=list
    )

    conditions: list[CreatePromotionConditionSchema] = Field(
        default_factory=list
    )

class PromotionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str
    description: str | None

    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    application_scope: PromotionApplicationScope

    priority: int

    starts_at: datetime | None
    ends_at: datetime | None

    is_active: bool

    pricing_rules: list[PricingRuleResponseSchema]
    audiences: list[PromotionAudienceResponseSchema]
    conditions: list[PromotionConditionResponseSchema]
    targets: list[PromotionTargetResponseSchema]

    created_at: datetime | None
    updated_at: datetime | None

class PromotionRowResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    description: str | None

    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    application_scope: PromotionApplicationScope
    priority: int

    starts_at: datetime | None
    ends_at: datetime | None
    is_active: bool

    status: str

    pricing_rules_count: int
    audiences_count: int
    targets_count: int
    conditions_count: int
    coupons_count: int

    has_coupon: bool

    created_at: datetime | None
    updated_at: datetime | None

class PromotionFiltersSchema(BaseModel):
    search: str | None = None

    sales_channel: SaleChannel | None = None
    application_scope: PromotionApplicationScope | None = None

    starts_at: date | None = None
    ends_at: date | None = None

class PromotionDetailResponseSchema(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    name: str
    description: str | None

    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    application_scope: PromotionApplicationScope

    priority: int

    starts_at: datetime | None
    ends_at: datetime | None

    is_active: bool

    pricing_rules: list[
        PricingRuleResponseSchema
    ]

    audiences: list[
        PromotionAudienceResponseSchema
    ]

    conditions: list[
        PromotionConditionResponseSchema
    ]

    coupons: list[
        CouponResponseSchema
    ]

    targets: list[
        PromotionTargetResponseSchema
    ]

    created_at: datetime | None
    updated_at: datetime | None

class UpdatePromotionSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    name: str | None = None
    description: str | None = None

    sales_channel: SaleChannel | None = None
    stacking_mode: PromotionStackingMode | None = None

    priority: int | None = None

    starts_at: datetime | None = None
    ends_at: datetime | None = None

    is_active: bool | None = None

class AppliedPromotionResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    promotion_id: int
    name: str
    discount_amount: Decimal