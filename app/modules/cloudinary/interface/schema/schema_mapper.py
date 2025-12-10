from app.shared.dto.cloudinary_dto import CloudinaryImageDTO
from app.modules.cloudinary.interface.schema.cloudinary_schema import ReadImageSchema


class CloudinarySchemaMapper:
    @staticmethod
    def to_schema(dto: CloudinaryImageDTO) -> ReadImageSchema:
        return ReadImageSchema(
            url=dto.url,
            public_id=dto.public_id
        )