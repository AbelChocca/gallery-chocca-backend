from app.domain.slide.slide_entity import SlideEntity
from app.infra.db.models.model_slide import SlideTable
from app.infra.db.mappers.base_mapper import BaseMapper

from typing import Optional

class SlideMapper(BaseMapper[SlideEntity, SlideTable]):
    @staticmethod
    def to_entity(model: SlideTable) -> SlideEntity:
        return SlideEntity(
            enlace_boton=model.button_href,
            activo=model.activo,
            orden=model.orden,
            fecha_actualizada=model.fecha_actualizada,
            fecha_creada=model.fecha_creada,
            id=model.id
        )

    @staticmethod
    def to_db_model(entity: SlideEntity, existing_model: Optional[SlideTable] = None) -> SlideTable:
        if existing_model:
            existing_model.button_href = entity.enlace_boton
            existing_model.activo = entity.activo
            existing_model.fecha_actualizada = entity.fecha_actualizada
            existing_model.fecha_creada = entity.fecha_creada
            existing_model.orden = entity.orden
            return existing_model
        return SlideTable(
            button_href=entity.enlace_boton,
            activo=entity.activo,
            orden=entity.orden,
            fecha_actualizada=entity.fecha_actualizada,
            fecha_creada=entity.fecha_creada
        )