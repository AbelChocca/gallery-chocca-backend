from app.infra.db.mappers.base_mapper import BaseMapper
from app.infra.db.models.model_media import MediaImageTable
from app.domain.media.entities.image import ImageEntity

class ImageMapper(BaseMapper[ImageEntity, MediaImageTable]):
    @staticmethod
    def to_db_model(entity: ImageEntity, existing_model: MediaImageTable | None = None) -> MediaImageTable:
        if existing_model:
            existing_model.alt_text = entity.alt_text
            existing_model.image_url = entity.image_url
            existing_model.owner_id = entity.owner_id
            existing_model.owner_type = entity.owner_type
            existing_model.public_id = entity.public_id
            return existing_model
        return MediaImageTable(
            public_id=entity.public_id,
            image_url=entity.image_url,
            alt_text=entity.alt_text,
            owner_type=entity.owner_type,
            owner_id=entity.owner_id
        )

    @staticmethod
    def to_entity(model: MediaImageTable) -> ImageEntity:
        return ImageEntity(
            id=model.id,
            image_url=model.image_url,
            owner_id=model.owner_id,
            owner_type=model.owner_type,
            public_id=model.public_id,
            alt_text=model.alt_text
        )