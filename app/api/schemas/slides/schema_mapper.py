from app.api.schemas.slides.slide_schema import PublishSlideSchema, ReadSlideSchema, SlideFilterSchema, UpdateSlideSchema
from app.application.slides.commands import PublishSlideCommand, SlideFiltersCommand, UpdateSlideCommand
from app.modules.slide.domain.dto import ReadSlideDTO

class InputSchemaMapper:
    @staticmethod
    def publish_command(publish_schema: PublishSlideSchema) -> PublishSlideCommand:
        return PublishSlideCommand(
            activo=publish_schema.activo,
            orden=publish_schema.orden,
            enlace_boton=publish_schema.enlace_boton
        )
    
    @staticmethod
    def to_filters_command(schema: SlideFilterSchema) -> SlideFiltersCommand:
        return SlideFiltersCommand(
            activo=schema.activo,
            fecha_creada=schema.fecha_creada,
            fecha_actualizada=schema.fecha_actualizada
        )
    
    @staticmethod
    def to_update_command(schema: UpdateSlideSchema) -> UpdateSlideCommand:
        return UpdateSlideCommand(
            enlace_boton=schema.enlace_boton,
            activo=schema.activo,
            orden=schema.orden,
            delete_image=schema.delete_image
        )
    
class OutputSchemaMapper:
    @staticmethod
    def to_schema(dto: ReadSlideDTO) -> ReadSlideSchema:
        return ReadSlideSchema(
            id=dto.id,
            imagen_url=dto.imagen_url,
            cloudinary_id=dto.cloudinary_id,
            enlace_boton=dto.enlace_boton,
            activo=dto.activo,
            orden=dto.orden,
            fecha_creada=dto.fecha_creada,
            fecha_actualizada=dto.fecha_actualizada
        )