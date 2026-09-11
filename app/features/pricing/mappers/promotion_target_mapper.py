from app.features.pricing.entities.promotion_target import (
    PromotionTarget,
)

from app.features.pricing.models.promotion_target import (
    PromotionTargetTable,
)

from app.infra.db.mappers.base_mapper import BaseMapper


class PromotionTargetMapper(
    BaseMapper[PromotionTarget, PromotionTargetTable]
):

    @staticmethod
    def to_db_model(
        entity: PromotionTarget,
        existing_model: PromotionTargetTable | None = None,
    ) -> PromotionTargetTable:

        model = existing_model or PromotionTargetTable()

        model.promotion_id = entity.promotion_id
        model.target_type = entity.target_type
        model.reference_id = entity.reference_id
        model.reference_value = entity.reference_value

        return model

    @staticmethod
    def to_entity(
        model: PromotionTargetTable,
    ) -> PromotionTarget:

        return PromotionTarget(
            id=model.id,
            promotion_id=model.promotion_id,
            target_type=model.target_type,
            reference_id=model.reference_id,
            reference_value=model.reference_value,
            created_at=model.created_at,
        )