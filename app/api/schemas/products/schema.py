from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from app.api.schemas.media.media_schema import ReadImage, UpdateImage

class ProductVariantRead(BaseModel):
    id: Optional[int] 
    product_id: Optional[int]
    color: str
    tallas: List[str]
    imagenes: List[ReadImage]

    model_config = ConfigDict(from_attributes=True)

class ProductRead(BaseModel):
    id: Optional[int] 
    nombre: str
    descripcion: str
    marca: str
    categoria: str   # Ej: "pantalon", "camisa"
    modelo: Optional[str]  # Ej: "jean", "drill"
    slug: Optional[str]
    precio: float
    descuento: Optional[float]
    promocion: Optional[bool]

    variants: List[ProductVariantRead]

    model_config = ConfigDict(from_attributes=True)

class CreateProductVariantSchema(BaseModel):
    color: str = Field(max_length=16, min_length=1)
    tallas: List[str] = Field(min_length=1)

class CreateProductSchema(BaseModel):
    nombre: str = Field(min_length=8, max_length=55)
    descripcion: str
    marca: str
    categoria: str = Field(min_length=4) # Ej: "pantalon", "camisa"
    modelo: Optional[str] = None  # Ej: "jean", "drill"
    precio: float = Field(ge=1, le=4999)
    descuento: Optional[float] = None
    promocion: Optional[bool] = None

    variants: List[CreateProductVariantSchema] = Field(min_length=1)

    temp_variants_id:List[int] = Field(min_length=1)

class UpdateProductVariantSchema(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    color: Optional[str] = Field(default=None, min_length=1, max_length=16, examples=[None])
    tallas: Optional[List[str]] = Field(default=None, min_length=1, examples=[None])
    imagenes: Optional[List[UpdateImage]] = Field(default=None, min_length=1)

    # flags
    to_delete: bool = False

class UpdateProductSchema(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = Field(default=None, min_length=8, max_length=55, examples=[None])
    descripcion: Optional[str] = Field(default=None, examples=[None])
    marca: Optional[str] = Field(default=None, examples=[None])
    categoria: Optional[str] = Field(default=None, min_length=4, examples=[None]) # Ej: "pantalon", "camisa"
    modelo: Optional[str] = Field(default=None, examples=[None])  # Ej: "jean", "drill"
    precio: Optional[float] = Field(default=None, ge=1, le=4999, examples=[None])
    descuento: Optional[float] = Field(default=None, examples=[0.0])
    promocion: Optional[bool] = Field(default=None, examples=[False])

    variants: Optional[List[UpdateProductVariantSchema]] = Field(default=None, min_length=1)
    temp_variants_id: Optional[List[int]] = Field(default=None)

    # flags
    name_changed: bool = False

class FilterSchema(BaseModel):
    name: Optional[str] = Field(default=None, examples=[None])
    marca: Optional[str] = Field(default=None, examples=[None])
    categoria: Optional[str] = Field(default=None, examples=[None])
    modelo: Optional[str] = Field(default=None, examples=[None])
    minPrice: Optional[float] = Field(default=None, ge=0, examples=[None])
    maxPrice: Optional[float] = Field(default=None, ge=1, le=4999, examples=[None])
    color: Optional[str] = Field(default=None, examples=[None])
    promocion: Optional[bool] = Field(default=None, examples=[None])

class GetProductsResponse(BaseModel):
    total: int
    productos: List[ProductRead]