from app.modules.slide.domain.slide_entity import SlideEntity
from app.modules.slide.infra.slide_model import SlideTable

from typing import Optional

class SlideMapper:
    @staticmethod
    def to_entity(slide_db: SlideTable) -> SlideEntity:
        return SlideEntity(
            imagen_url=slide_db.imagen_url,
            enlace_boton=slide_db.enlace_boton,
            activo=slide_db.activo,
            cloudinary_id=slide_db.cloudinary_id,
            orden=slide_db.orden,
            fecha_actualizada=slide_db.fecha_actualizada,
            fecha_creada=slide_db.fecha_creada,
            id=slide_db.id
        )

    @staticmethod
    def to_db_model(slide: SlideEntity, slide_db: Optional[SlideTable] = None) -> SlideTable:
        if slide_db:
            slide_db.imagen_url = slide.imagen_url
            slide_db.enlace_boton = slide.enlace_boton
            slide_db.activo = slide.activo
            slide_db.fecha_actualizada = slide.fecha_actualizada
            slide_db.fecha_creada = slide.fecha_creada
            slide_db.orden = slide.orden
            slide_db.cloudinary_id = slide.cloudinary_id
            return slide_db
        return SlideTable(
            imagen_url=slide.imagen_url,
            enlace_boton=slide.enlace_boton,
            cloudinary_id=slide.cloudinary_id,
            activo=slide.activo,
            orden=slide.orden,
            fecha_actualizada=slide.fecha_actualizada,
            fecha_creada=slide.fecha_creada
        )