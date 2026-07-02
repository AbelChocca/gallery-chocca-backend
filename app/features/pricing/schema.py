from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

from app.shared.pagination.schema import PaginationResponseSchema
from app.features.pricing.types import PricingRuleType

class CreatePricingRuleRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    type: PricingRuleType = Field(..., description="Tipo de regla de pricing (discount, markup, etc.)")
    value: Decimal = Field(..., gt=0)
    priority: int = Field(default=0, ge=0)

    is_active: bool = True
    is_stackable: bool = True

class PricingRuleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    type: PricingRuleType
    value: Decimal

    is_active: bool
    is_stackable: bool
    priority: int

    starts_at: datetime | None = None
    ends_at: datetime | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

class PricingRuleFilterSchema(BaseModel):
    is_active: bool | None = None
    type: str | None = None

    priority_min: int | None = Field(default=None, ge=0)
    priority_max: int | None = Field(default=None, ge=0)

    search: str | None = Field(default=None, max_length=100)

class PricingRuleListResponse(BaseModel):
    total: int
    items: list[PricingRuleResponse]
    pagination: PaginationResponseSchema

class ProductRuleBatchRequest(BaseModel):
    product_ids: list[int] = Field(..., min_length=1)
    rule_id: int = Field(..., gt=0)

# PRODUCT PRICING

class ProductPricingSummarySchema(BaseModel):
    id: int
    nombre: str
    categoria: str
    image_url: str | None
    base_price: Decimal
    is_active: bool
    final_price: Decimal
    latest_applied_rule: PricingRuleResponse | None

class ProductAppliedPricingRuleResponse(BaseModel):
    product_id: int
    assigned_at: datetime

    pricing_rule: PricingRuleResponse

class ProductPricingDetailResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    base_price: Decimal
    is_active: bool
    image_url: str | None = None

    applied_rules: list[ProductAppliedPricingRuleResponse]

    final_price: Decimal

class ProductsPricingSummaryResponse(BaseModel):
    total_items: int
    items: list[ProductPricingSummarySchema]
    pagination: PaginationResponseSchema

class ProductsPricingRulesResponse(BaseModel):
    total_items: int
    items: list[ProductAppliedPricingRuleResponse]
    pagination: PaginationResponseSchema