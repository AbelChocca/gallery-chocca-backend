from dataclasses import dataclass

@dataclass(frozen=True)
class PromotionPricingRuleAssignment:
    pricing_rule_id: int
    execution_order: int