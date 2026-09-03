from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.models.model_promotion import PromotionTable
from app.infra.db.mappers.base_mapper import BaseMapper

class PromotionMapper(BaseMapper[Promotion, PromotionTable]):

    @staticmethod
    def to_db_model(
        entity: Promotion,
        existing_model: PromotionTable | None = None,
    ) -> PromotionTable:

        model = existing_model or PromotionTable()

        model.name = entity.name
        model.description = entity.description
        model.sales_channel = entity.sales_channel
        model.stacking_mode = entity.stacking_mode
        model.priority = entity.priority
        model.starts_at = entity.starts_at
        model.ends_at = entity.ends_at
        model.is_active = entity.is_active

        return model

    @staticmethod
    def to_entity(
        model: PromotionTable,
    ) -> Promotion:

        return Promotion(
            id=model.id,
            name=model.name,
            description=model.description,
            sales_channel=model.sales_channel,
            stacking_mode=model.stacking_mode,
            priority=model.priority,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )