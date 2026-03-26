from typing import Dict, Any
from datetime import datetime, timezone

from app.domain.media.entities.image import ImageEntity
from app.core.exceptions import ValidationError, ValueNotFound

class SlideEntity:
    _UPDATE_ATTRIBUTES = {"activo", "enlace_boton"}
    def __init__(
        self,
        id: int | None = None,
        activo: bool = True,
        orden: int | None = None,
        enlace_boton: str | None = None,
        fecha_creada: datetime | None = None,
        fecha_actualizada: datetime | None = None
    ):
        self.id = id
        self._image: ImageEntity | None = None
        self.enlace_boton = enlace_boton
        self.activo = activo
        self._orden = orden or 0

        # Manejo de timestamps
        ahora = datetime.now(timezone.utc)
        self.fecha_creada = fecha_creada or ahora
        self.fecha_actualizada = fecha_actualizada or ahora

    @property
    def has_image(self) -> bool:
        return self.image is not None
    
    @property
    def image(self) -> ImageEntity:
        return self._image
    
    @property
    def orden(self) -> int:
        return self._orden
    
    @orden.setter
    def orden(self, new_order: int) -> None:
        if not isinstance(new_order, int):
            raise ValidationError(
                "'new_order' must be an integer",
                {
                    "entity": "SlideEntity",
                    "event": "orden.setter",
                    "new_order_type": type(new_order).__name__
                }
                )
        if new_order <= 0:
            raise ValidationError(
                "'new_order' must be greater than 0",
                {
                    "entity": "SlideEntity",
                    "event": "orden.setter",
                    "new_order": new_order
                }
                )
        self._orden = new_order
    
    @image.setter
    def image(self, new_image: ImageEntity | None) -> None:
        if new_image is None:
            self._image = new_image
            return
        
        if not isinstance(new_image, ImageEntity):
            raise ValidationError(
                "'new_image' must be an ImageEntity",
                {
                    "entity": "SlideEntity",
                    "event": "image.setter",
                    "new_image_type": type(new_image).__name__
                }
            )
        self._image = new_image
    
    @property
    def image_public_id(self) -> str:
        return self.image.public_id
    
    @property
    def to_dict(self) -> dict:
        image = self.image
        data = {
            "id": self.id,
            "activo": self.activo,
            "orden": self.orden,
            "enlace_boton": self.enlace_boton
        }

        if image is not None:
            # Mapear solo los atributos esenciales de la image
            data["image"] = self.image.to_dict

        return data
    
    @property
    def is_inactive(self) -> dict:
        return self.activo is False

    def _update_timestamp(self):
        """Update the date to current date"""
        self.fecha_actualizada = datetime.now(timezone.utc)

    def toggle_activation(self, value: bool):
        self.activo = value

    def sync_image(self, key_values: Dict[int, ImageEntity]) -> None:
        image = key_values.get(self.id)
        if not image:
            raise ValueNotFound(
                "Owner id of image wasn't found for slide",
                {
                    "entity": "Slide",
                    "event": "sync_image",
                    "slide_id": self.id,
                }
            )
        self.image = image

    def update_slide(self, obj: Dict[str, Any]):
        if not isinstance(obj, dict):
            raise ValidationError(
                "'obj' must be a dict",
                {
                    "entity": "Slide",
                    "event": "update_slide",
                    "invalid_obj_type": type(obj).__name__
                }
                )
        if not obj:
            raise ValidationError(
                "'obj' mustn't be empty",
                {
                    "entity": "Slide",
                    "event": "update_slide"
                }
                )
        
        for key, value in obj.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)

        self._update_timestamp()