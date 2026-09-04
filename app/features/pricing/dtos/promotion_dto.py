from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from app.features.pricing.entities.promotion import Promotion

from app.features.pricing.types.promotion_types import PromotionTargetType, PromotionAudienceType, PromotionStackingMode
from app.features.pricing.dtos.promotion_condition import AppliedPromotionConditionDTO
from app.features.sales.types.sale import SaleChannel

from app.features.pricing.dtos.pricing_rule_dto import AppliedPricingRuleDTO
from app.features.products.types import BrandType, CategoryType

@dataclass(slots=True)
class PromotionProductCandidateDTO:
    product_id: int
    promotion: Promotion

@dataclass(slots=True)
class PricingProduct:
    product_id: int
    quantity: int
    unit_price: Decimal
    
    promotions: list[Promotion]

@dataclass(slots=True)
class AppliedPromotionTargetDTO:
    type: PromotionTargetType

    ids: list[int]

@dataclass(slots=True)
class AppliedPromotionAudienceDTO:
    type: PromotionAudienceType

    ids: list[int] | None = None

@dataclass(slots=True)
class PromotionCandidateCriteria:
    product_ids: list[int]

    categories: dict[int, CategoryType]
    brands: dict[int, BrandType]

    sale_channel: SaleChannel


@dataclass(slots=True)
class AppliedPromotionDTO:
    id: int

    priority: int

    stacking_mode: PromotionStackingMode

    starts_at: datetime

    ends_at: datetime | None

    target: AppliedPromotionTargetDTO

    audience: AppliedPromotionAudienceDTO

    conditions: list[AppliedPromotionConditionDTO]

    pricing_rules: list[AppliedPricingRuleDTO]  

