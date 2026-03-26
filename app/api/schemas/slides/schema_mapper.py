from app.api.schemas.slides.slide_schema import PublishSlideSchema, SlideFilterSchema, UpdateSlideSchema, UpdateSlidesOrderSchema
from app.domain.slide.slide_dto import PublishSlideCommand, SlideFiltersCommand, UpdateSlideCommand
from app.domain.slide.slide_dto import UpdateSlidesOrder, UpdateOrder

class InputSchemaMapper:
    @staticmethod
    def to_update_order(update_order: UpdateSlidesOrderSchema) -> UpdateSlidesOrder:
        return UpdateSlidesOrder(
            slides=[
                UpdateOrder(slide.id, slide.new_order)
                for slide in update_order.slides
            ]
        )
    
    @staticmethod
    def publish_command(publish_schema: PublishSlideSchema) -> PublishSlideCommand:
        return PublishSlideCommand(
            activo=publish_schema.activo,
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