from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ReadSlideDTO:
    imagen_url: str
    activo: bool
    orden: int
    cloudinary_id: str
    id: Optional[int] = None
    enlace_boton: Optional[str] = None
    fecha_creada: Optional[datetime] = None
    fecha_actualizada: Optional[datetime] = None

@dataclass
class UpdateSlideDTO:
    enlace_boton: Optional[str] = None
    activo: Optional[bool] = None
    orden: Optional[int] = None

@dataclass
class SlideFilterDTO:
    activo: Optional[bool] = None
    fecha_creada: Optional[datetime] = None
    fecha_actualizada: Optional[datetime] = None