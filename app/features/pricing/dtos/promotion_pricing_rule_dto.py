from dataclasses import dataclass
from app.features.pricing.types.pricing_rules_types import PricingRuleType
from app.features.pricing.dtos.pricing_rule_dto import PricingRuleParameters

@dataclass(frozen=True)
class PromotionPricingRuleAssignment:
    pricing_rule_id: int
    execution_order: int

@dataclass(frozen=True, slots=True)
class CreatePromotionPricingRuleAssignment:
    name: str
    type: PricingRuleType
    parameters: PricingRuleParameters
    execution_order: int
    description: str | None = None

@dataclass(slots=True)
class ExistingPromotionPricingRuleDTO:
    pricing_rule_id: int
    execution_order: int = 0


@dataclass(slots=True)
class NewPromotionPricingRuleDTO:
    name: str
    type: PricingRuleType
    parameters: PricingRuleParameters
    execution_order: int = 0
    description: str | None = None


PromotionPricingRuleDTO = (
    ExistingPromotionPricingRuleDTO
    | NewPromotionPricingRuleDTO
)