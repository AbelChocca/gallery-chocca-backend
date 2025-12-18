from app.modules.cloudinary.domain.dto import CloudinaryImageDTO
from app.api.schemas.cloudinary.cloudinary_schema import ReadImageSchema

class OutputSchemaMapper:
    @staticmethod
    def to_schema(dto: CloudinaryImageDTO) -> ReadImageSchema:
        return ReadImageSchema(
            url=dto.url,
            public_id=dto.public_id
        )