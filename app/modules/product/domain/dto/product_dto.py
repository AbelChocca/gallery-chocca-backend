from dataclasses import dataclass
from typing import List, Optional

from app.modules.product.domain.dto.variant_dto import ReadProductVariantDTO, UpdateProductVariantDTO

@dataclass
class ReadProductDTO:
    id: int
    nombre: str
    descripcion: str
    categoria: str
    marca: str
    modelo: str
    precio: float
    descuento: float
    slug: str
    promocion: bool

    variants: List[ReadProductVariantDTO]

@dataclass
class FilterSchemaDTO:
    name: Optional[str] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    modelo: Optional[str] = None
    minPrice: Optional[float] = None
    maxPrice: Optional[float] = None
    color: Optional[str] = None
    promocion: Optional[bool] = None

@dataclass
class UpdateProductDTO:
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    modelo: Optional[str] = None
    precio: Optional[float] = None
    descuento: Optional[float] = None
    promocion: Optional[bool] = None

    variants: List[UpdateProductVariantDTO]