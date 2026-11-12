from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.pricing.entities.promotion_pricing_rule import (
    PromotionPricingRule,
)

from app.features.pricing.models.promotion_pricing_rule import (
    PromotionPricingRuleTable,
)


class PromotionPricingRuleMapper(
    BaseMapper[
        PromotionPricingRule,
        PromotionPricingRuleTable,
    ]
):

    @staticmethod
    def to_db_model(
        entity: PromotionPricingRule,
        existing_model: PromotionPricingRuleTable | None = None,
    ) -> PromotionPricingRuleTable:

        model = existing_model or PromotionPricingRuleTable()

        model.promotion_id = entity.promotion_id
        model.pricing_rule_id = entity.pricing_rule_id
        model.execution_order = entity.execution_order

        return model

    @staticmethod
    def to_entity(
        model: PromotionPricingRuleTable,
    ) -> PromotionPricingRule:

        return PromotionPricingRule(
            promotion_id=model.promotion_id,
            pricing_rule_id=model.pricing_rule_id,
            execution_order=model.execution_order,
            assigned_at=model.assigned_at,
        )