from dataclasses import dataclass
from typing import List, Optional

from app.shared.dto.color_variant_dto import ColorVariantDTO, UpdateProductColorVariantDTO

@dataclass
class ProductDTO:
    nombre: str
    descripcion: str
    categoria: str
    marca: str
    modelo: str
    precio: float
    descuento: float
    promocion: bool

    variants: List[ColorVariantDTO]

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
    id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    modelo: Optional[str] = None
    precio: Optional[float] = None
    descuento: Optional[float] = None
    promocion: Optional[bool] = None

    variants: Optional[List[UpdateProductColorVariantDTO]] = None