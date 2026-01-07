from app.domain.slide.slide_entity import SlideEntity
from app.infra.db.models.slide_model import SlideTable
from app.infra.db.mappers.base_mapper import BaseMapper

from typing import Optional

class SlideMapper(BaseMapper[SlideEntity, SlideTable]):
    @staticmethod
    def to_entity(model: SlideTable) -> SlideEntity:
        return SlideEntity(
            imagen_url=model.imagen_url,
            enlace_boton=model.enlace_boton,
            activo=model.activo,
            cloudinary_id=model.cloudinary_id,
            orden=model.orden,
            fecha_actualizada=model.fecha_actualizada,
            fecha_creada=model.fecha_creada,
            id=model.id
        )

    @staticmethod
    def to_db_model(entity: SlideEntity, existing_model: Optional[SlideTable] = None) -> SlideTable:
        if existing_model:
            existing_model.imagen_url = entity.imagen_url
            existing_model.enlace_boton = entity.enlace_boton
            existing_model.activo = entity.activo
            existing_model.fecha_actualizada = entity.fecha_actualizada
            existing_model.fecha_creada = entity.fecha_creada
            existing_model.orden = entity.orden
            existing_model.cloudinary_id = entity.cloudinary_id
            return existing_model
        return SlideTable(
            imagen_url=entity.imagen_url,
            enlace_boton=entity.enlace_boton,
            cloudinary_id=entity.cloudinary_id,
            activo=entity.activo,
            orden=entity.orden,
            fecha_actualizada=entity.fecha_actualizada,
            fecha_creada=entity.fecha_creada
        )