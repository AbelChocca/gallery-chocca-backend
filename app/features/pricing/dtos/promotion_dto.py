from dataclasses import dataclass, field
from datetime import datetime
from app.features.pricing.entities.promotion import Promotion

from app.features.pricing.types.promotion_types import PromotionStackingMode, PromotionApplicationScope
from app.features.sales.types.sale import SaleChannel

from app.features.products.types import BrandType, CategoryType
from app.features.pricing.dtos.promotion_condition import CreatePromotionConditionDTO
from app.features.pricing.dtos.promotion_audience_dto import CreatePromotionAudienceDTO
from app.features.pricing.dtos.promotion_target import CreatePromotionTargetDTO
from app.features.pricing.dtos.promotion_pricing_rule_dto import PromotionPricingRuleDTO

@dataclass(slots=True)
class PromotionProductCandidateDTO:
    product_id: int
    promotion: Promotion


@dataclass(slots=True)
class PromotionCandidateCriteria:
    product_ids: list[int]

    categories: dict[int, CategoryType]
    brands: dict[int, BrandType]

    sale_channel: SaleChannel 

@dataclass(slots=True)
class CreatePromotionDTO:
    name: str
    description: str | None
    sales_channel: SaleChannel
    stacking_mode: PromotionStackingMode
    application_scope: PromotionApplicationScope
    priority: int = 0
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    is_active: bool = True

    pricing_rules: list[
        PromotionPricingRuleDTO
    ] = field(default_factory=list)

    audiences: list[CreatePromotionAudienceDTO] = field(
        default_factory=list
    )

    targets: list[CreatePromotionTargetDTO] = field(
        default_factory=list
    )

    conditions: list[CreatePromotionConditionDTO] = field(
        default_factory=list
    )

@dataclass(slots=True)
class PromotionRowDTO:
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