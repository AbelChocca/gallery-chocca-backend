from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class SlideDTO:
    imagen_url: str
    activo: bool
    orden: int
    cloudinary_id: str
    id: Optional[int] = None
    enlace_boton: Optional[str] = None
    fecha_creada: Optional[datetime] = None
    fecha_actualizada: Optional[datetime] = None

@dataclass
class SlideFiltersDTO:
    activo: Optional[bool] = None
    fecha_creada: Optional[datetime] = None
    fecha_actualizada: Optional[datetime] = None

@dataclass
class UpdateSlideDTO:
    imagen_url: Optional[str] = None
    cloudinary_id: Optional[str] = None
    enlace_boton: Optional[str] = None
    activo: Optional[bool] = None
    orden: Optional[int] = None