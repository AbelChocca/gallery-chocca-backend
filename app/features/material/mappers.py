from app.features.material.schema import MaterialResponseSchema, MaterialPaginatedResponseSchema, MaterialCatalogResponseSchema
from app.features.media.schema import ReadImage
from app.features.material.dto import MaterialCatalogDTO
from app.shared.pagination.schema import PaginationResponseSchema

from app.features.material.schema import MaterialResponseSchema
from app.features.media.schema import ReadImage
from app.features.material.dto import MaterialResponseDTO


class MaterialResponseMapper:
    @staticmethod
    def to_schema(dto: MaterialResponseDTO) -> MaterialResponseSchema:
        return MaterialResponseSchema(
            id=dto.id,
            code=dto.code,
            name=dto.name,
            description=dto.description,
            company=dto.company,
            stock=dto.stock,
            material_type=dto.material_type,
            unit_type=dto.unit_type,
            minimum_stock=dto.minimum_stock,
            is_active=dto.is_active,
            availability_status=dto.availability_status,
            image=(
                ReadImage(
                    id=dto.image.id,
                    image_url=dto.image.image_url,
                    public_id=dto.image.public_id,
                    owner_id=dto.image.owner_id,
                )
                if dto.image
                else None
            ),
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
    
class MaterialPaginatedResponseMapper:
    @staticmethod
    def to_schema(
        entities: list[MaterialCatalogDTO],
        total_items: int,
        total_pages: int,
        current_page: int,
    ) -> MaterialPaginatedResponseSchema:

        items = [
            MaterialCatalogResponseSchema(
                id=entity.id,
                code=entity.code,
                name=entity.name,
                material_type=entity.material_type,
                unit_type=entity.unit_type,
                stock=entity.stock,
                minimum_stock=entity.minimum_stock,
                is_active=entity.is_active,
                availability_status=entity.availability_status,
                image=(
                    ReadImage(
                        image_url=entity.image.image_url,
                        id=entity.image.id,
                        public_id=entity.image.public_id,
                        owner_id=entity.image.owner_id,
                        alt_text=entity.image.alt_text,
                    )
                    if entity.image
                    else None
                ),
            )
            for entity in entities
        ]

        return MaterialPaginatedResponseSchema(
            items=items,
            total_items=total_items,
            pagination=PaginationResponseSchema(
                total_pages=total_pages,
                current_page=current_page
            ),
        )