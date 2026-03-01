from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime
from datetime import datetime, timezone

class SlideTable(SQLModel, table=True):
    __tablename__ = "slide"

    id: int | None = Field(default=None, primary_key=True)
    activo: bool = Field(default=True, index=True)
    orden: int = Field(default=0, unique=True)
    button_href: str | None = Field(default=None)
    fecha_creada: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))
    fecha_actualizada: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))