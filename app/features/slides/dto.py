from dataclasses import dataclass, asdict, field
from typing import List
from datetime import datetime

@dataclass
class UpdateOrder:
    b_id: int
    new_order: int

    @property
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class UpdateSlidesOrder:
    slides: List[UpdateOrder] | None = None

    @property
    def ids(self) -> list[int]:
        return [e.b_id for e in self.slides]
    
    @property
    def positions(self) -> list[int]:
        return [slide.new_order for slide in self.slides]

@dataclass
class SlideFiltersCommand:
    activo: bool | None = None
    fecha_creada: datetime | None = None
    fecha_actualizada: datetime | None = None

    @property
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class PublishSlideCommand:
    activo: bool
    enlace_boton: str | None = None

@dataclass
class UpdateSlideCommand:
    enlace_boton: str | None = None
    activo: bool | None = None
    orden: int | None = None

    # flags
    delete_image: bool = False

    @property
    def to_dict(self) -> dict:
        return asdict(self)
    
@dataclass(slots=True)
class SlidesOverviewDTO:
    total: int = 0
    active: int = 0
    inactive: int = 0
    recent: list[dict] = field(default_factory=list)