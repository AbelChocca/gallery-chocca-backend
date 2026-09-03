from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.infra.db.mappers.base_mapper import BaseMapper

class PricingRuleMapper(
    BaseMapper[PricingRule, PricingRuleTable]
):

    @staticmethod
    def to_db_model(
        entity: PricingRule,
        existing_model: PricingRuleTable | None = None,
    ) -> PricingRuleTable:

        model = existing_model or PricingRuleTable()

        model.name = entity.name
        model.description = entity.description
        model.type = entity.type
        model.parameters = entity.parameters

        return model

    @staticmethod
    def to_entity(
        model: PricingRuleTable,
    ) -> PricingRule:

        return PricingRule(
            id=model.id,
            name=model.name,
            description=model.description,
            type=model.type,
            parameters=model.parameters,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )