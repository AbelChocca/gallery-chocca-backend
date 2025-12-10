from typing import Optional
from datetime import datetime, timezone
from dataclasses import asdict

from app.shared.dto.slide_dto import UpdateSlideDTO

class SlideEntity:
    def __init__(
        self,
        imagen_url: str,
        cloudinary_id: str,
        id: Optional[int] = None,
        enlace_boton: Optional[str] = None,
        activo: bool = True,
        orden: int = 0,
        fecha_creada: Optional[datetime] = None,
        fecha_actualizada: Optional[datetime] = None
    ):
        self.id = id
        self.cloudinary_id = cloudinary_id
        self.imagen_url = imagen_url
        self.enlace_boton = enlace_boton
        self.activo = activo
        self.orden = orden

        # Manejo de timestamps
        ahora = datetime.now(timezone.utc)
        self.fecha_creada = fecha_creada or ahora
        self.fecha_actualizada = fecha_actualizada or ahora

    def actualizar_timestamp(self):
        """Actualiza la fecha_actualizada al momento actual."""
        self.fecha_actualizada = datetime.now(timezone.utc)

    def update_slide(self, dto: UpdateSlideDTO):
        """
        Updates the entity using a dataclass DTO.
        Only updates fields that are not None.
        """
        update_data = {k: v for k, v in asdict(dto).items() if v is not None}

        for key, value in update_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.actualizar_timestamp()