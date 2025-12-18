from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class PublishSlideSchema(BaseModel):
    orden: int = Field(ge=0)
    enlace_boton: Optional[str] = None
    activo: bool = True

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
    enlace_boton: Optional[str] = None
    activo: Optional[bool] = None
    orden: Optional[int] = None

    # flags
    delete_image: bool = False

class SlideFilterSchema(BaseModel):
    activo: Optional[bool] = Field(default=None, examples=[None])
    fecha_creada: Optional[datetime] = Field(default=None, examples=[None])
    fecha_actualizada: Optional[datetime] = Field(default=None, examples=[None])