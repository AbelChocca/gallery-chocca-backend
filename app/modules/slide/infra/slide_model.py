from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime
from typing import Optional
from datetime import datetime, timezone

class SlideTable(SQLModel, table=True):
    __tablename__ = "slide"

    id: Optional[int] = Field(default=None, primary_key=True)
    imagen_url: str = Field(max_length=255, nullable=False)
    enlace_boton: Optional[str] = Field(default=None)
    activo: bool = Field(default=True, index=True)
    cloudinary_id: str = Field(nullable=False)
    orden: int = Field(default=0)
    fecha_creada: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))
    fecha_actualizada: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))