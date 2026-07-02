from app.features.pricing.entities.product_pricing_rule import ProductPricingRule
from app.infra.db.models.model_product_pricing_rule import ProductPricingRuleTable
from app.infra.db.mappers.base_mapper import BaseMapper


class ProductPricingRuleMapper(BaseMapper[ProductPricingRule, ProductPricingRuleTable]):

    @staticmethod
    def to_db_model(
        entity: ProductPricingRule,
        existing_model: ProductPricingRuleTable | None = None
    ) -> ProductPricingRuleTable:

        model = existing_model or ProductPricingRuleTable()

        model.product_id = entity.product_id
        model.pricing_rule_id = entity.pricing_rule_id

        return model

    @staticmethod
    def to_entity(model: ProductPricingRuleTable) -> ProductPricingRule:
        return ProductPricingRule(
            product_id=model.product_id,
            pricing_rule_id=model.pricing_rule_id,
            assigned_at=model.assigned_at,
        )