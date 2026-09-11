from app.features.pricing.entities.promotion_condition import (
    PromotionCondition,
)
from app.features.pricing.models.promotion_condition import (
    PromotionConditionTable,
)
from app.infra.db.mappers.base_mapper import BaseMapper


class PromotionConditionMapper(
    BaseMapper[PromotionCondition, PromotionConditionTable]
):

    @staticmethod
    def to_db_model(
        entity: PromotionCondition,
        existing_model: PromotionConditionTable | None = None,
    ) -> PromotionConditionTable:
        model = existing_model or PromotionConditionTable()

        model.promotion_id = entity.promotion_id
        model.condition_type = entity.condition_type
        model.parameters = entity.parameters
        model.description = entity.description

        return model

    @staticmethod
    def to_entity(
        model: PromotionConditionTable,
    ) -> PromotionCondition:
        return PromotionCondition(
            id=model.id,
            promotion_id=model.promotion_id,
            condition_type=model.condition_type,
            parameters=model.parameters,
            description=model.description,
            created_at=model.created_at,
        )