from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SlideFiltersCommand:
    activo: Optional[bool] = None
    fecha_creada: Optional[datetime] = None
    fecha_actualizada: Optional[datetime] = None

@dataclass
class PublishSlideCommand:
    activo: bool
    orden: int
    enlace_boton: Optional[str] = None

@dataclass
class UpdateSlideCommand:
    enlace_boton: Optional[str] = None
    activo: Optional[bool] = None
    orden: Optional[int] = None

    # flags
    delete_image: bool = False