from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List

from app.api.schemas.media.media_schema import ReadImage
from app.api.schemas.pagination import PaginationResponseSchema

class PublishSlideSchema(BaseModel):
    enlace_boton: str | None = None
    activo: bool = True

class ReadSlideSchema(BaseModel):
    id: int
    image: ReadImage
    enlace_boton: str | None = None
    activo: bool
    orden: int

    model_config = ConfigDict(from_attributes=True)

class UpdateOrder(BaseModel):
    id: int
    new_order: int

class UpdateSlidesOrderSchema(BaseModel):
    slides: List[UpdateOrder] | None = None

class GetSlidesResponseSchema(BaseModel):
    slides: List[ReadSlideSchema]
    pagination: PaginationResponseSchema

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