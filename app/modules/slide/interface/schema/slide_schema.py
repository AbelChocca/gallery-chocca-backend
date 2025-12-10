from pydantic import BaseModel, constr, Field, ConfigDict, conint
from datetime import datetime, timezone
from typing import Optional, Annotated


class PublishSlideSchema(BaseModel):
    imagen_url: Annotated[str, constr(max_length=255)]
    orden: Annotated[int, conint(ge=0)]
    cloudinary_id: str
    enlace_boton: Optional[str] = None
    activo: bool = True
    fecha_creada: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizada: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReadSlideSchema(BaseModel):
    id: int
    imagen_url: str
    cloudinary_id: str
    enlace_boton: Optional[str] = None
    activo: bool
    orden: int
    fecha_creada: datetime
    fecha_actualizada: datetime

    model_config = ConfigDict(from_attributes=True)

class UpdateSlideSchema(BaseModel):
    imagen_url: Optional[Annotated[str, constr(max_length=255)]] = None
    cloudinary_id: Optional[str] = None
    enlace_boton: Optional[str] = None
    activo: Optional[bool] = None
    orden: Optional[int] = None

class SlideFilterSchema(BaseModel):
    activo: Optional[bool] = None
    fecha_creada: Optional[datetime] = None
    fecha_actualizada: Optional[datetime] = None