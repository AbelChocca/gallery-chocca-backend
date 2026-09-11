from app.features.pricing.entities.promotion_audience import PromotionAudience
from app.features.pricing.models.promotion_audience import PromotionAudienceTable
from app.infra.db.mappers.base_mapper import BaseMapper


class PromotionAudienceMapper(
    BaseMapper[PromotionAudience, PromotionAudienceTable]
):

    @staticmethod
    def to_db_model(
        entity: PromotionAudience,
        existing_model: PromotionAudienceTable | None = None,
    ) -> PromotionAudienceTable:
        model = existing_model or PromotionAudienceTable()

        model.promotion_id = entity.promotion_id
        model.audience_type = entity.audience_type
        model.reference_id = entity.reference_id
        model.reference_value = entity.reference_value

        return model

    @staticmethod
    def to_entity(
        model: PromotionAudienceTable,
    ) -> PromotionAudience:
        return PromotionAudience(
            id=model.id,
            promotion_id=model.promotion_id,
            audience_type=model.audience_type,
            reference_id=model.reference_id,
            reference_value=model.reference_value,
            created_at=model.created_at,
        )