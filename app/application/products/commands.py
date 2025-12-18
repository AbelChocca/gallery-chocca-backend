from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PublishProductVariantCommand:
    color: str
    tallas: List[str]

@dataclass 
class PublishProductCommand:
    nombre: str
    descripcion: str
    categoria: str
    marca: str
    modelo: str
    precio: float
    descuento: float
    promocion: bool

    variants: List[PublishProductVariantCommand]

    temp_variants_id: List[int]

@dataclass
class UpdateVariantImageCommand:
    id: Optional[int] = None
    variant_id: Optional[int] = None
    url: Optional[str] = None
    cloudinary_id: Optional[str] = None

    # flags
    to_delete: bool = False

@dataclass
class UpdateProductVariantCommand:
    id: Optional[int] = None
    product_id: Optional[int] = None
    color: Optional[str] = None
    tallas: Optional[List[str]] = None
    imagenes: Optional[List[UpdateVariantImageCommand]] = None

    # flags
    to_delete: bool = False

@dataclass
class UpdateProductCommand:
    variants: List[UpdateProductVariantCommand]
    id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    modelo: Optional[str] = None
    precio: Optional[float] = None
    descuento: Optional[float] = None
    promocion: Optional[bool] = None
    temp_variants_id: Optional[List[int]] = None

    # flags
    name_changed: bool = False

@dataclass
class FilterProductCommand:
    name: Optional[str] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    modelo: Optional[str] = None
    minPrice: Optional[float] = None
    maxPrice: Optional[float] = None
    color: Optional[str] = None
    promocion: Optional[bool] = None