from app.domain.media.media_dto import ReadMediaImageDTO
from app.api.schemas.media.media_schema import ReadImage

class OutputSchemaMapper:
    @staticmethod
    def to_schema(dto: ReadMediaImageDTO) -> ReadImage:
        return ReadImage(
            image_url=dto.image_url,
            owner_id=dto.owner_id,
            public_id=dto.public_id,
            owner_type=dto.owner_type,
            id=dto.id,
            alt_text=dto.alt_text
        )