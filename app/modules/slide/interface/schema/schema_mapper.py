from app.modules.slide.interface.schema.slide_schema import PublishSlideSchema, ReadSlideSchema, SlideFilterSchema
from app.modules.slide.domain.slide_entity import SlideEntity
from app.shared.dto.slide_dto import SlideDTO, SlideFiltersDTO

class SlideSchemaMapper:
    @staticmethod
    def publish_dto(publish_schema: PublishSlideSchema) -> SlideDTO:
        return SlideDTO(
            imagen_url=publish_schema.imagen_url,
            enlace_boton=publish_schema.enlace_boton,
            cloudinary_id=publish_schema.cloudinary_id,
            activo=publish_schema.activo,
            orden=publish_schema.orden,
            fecha_actualizada=publish_schema.fecha_actualizada,
            fecha_creada=publish_schema.fecha_creada
        )
    
    @staticmethod
    def entity_to_schema(entity: SlideEntity) -> ReadSlideSchema:
        return ReadSlideSchema(
            id=entity.id,
            imagen_url=entity.imagen_url,
            cloudinary_id=entity.cloudinary_id,
            enlace_boton=entity.enlace_boton,
            activo=entity.activo,
            orden=entity.orden,
            fecha_actualizada=entity.fecha_actualizada,
            fecha_creada=entity.fecha_creada
        )
    
    @staticmethod
    def to_filters_dto(schema: SlideFilterSchema) -> SlideFiltersDTO:
        return SlideFiltersDTO(
            activo=schema.activo,
            fecha_actualizada=schema.fecha_actualizada,
            fecha_creada=schema.fecha_creada
        )