from app.features.pricing.entities.pricing_rule import PricingRule
from app.infra.db.models.model_pricing_rule import PricingRuleTable
from app.infra.db.mappers.base_mapper import BaseMapper

class PricingRuleMapper(BaseMapper[PricingRule, PricingRuleTable]):

    @staticmethod
    def to_db_model(entity: PricingRule, existing_model: PricingRuleTable | None = None) -> PricingRuleTable:
        model = existing_model or PricingRuleTable()

        model.name = entity.name
        model.description = entity.description
        model.type = entity.type
        model.value = entity.value
        model.is_stackable = entity.is_stackable
        model.is_active = entity.is_active
        model.priority = entity.priority
        model.starts_at = entity.starts_at
        model.ends_at = entity.ends_at

        return model

    @staticmethod
    def to_entity(model: PricingRuleTable) -> PricingRule:
        return PricingRule(
            id=model.id,
            name=model.name,
            description=model.description,
            type=model.type,
            value=model.value,
            is_active=model.is_active,
            is_stackable=model.is_stackable,
            priority=model.priority,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )