from pydantic import BaseModel, Field, ConfigDict
from typing import List

from app.api.schemas.media.media_schema import ReadImage, UpdateImage
from app.api.schemas.pagination import PaginationResponseSchema
from app.domain.product.dto.product_dto import ColorFilter, BrandType, CategoryType, SizeType

class VariantSizeRead(BaseModel):
    id: int
    variant_id: int
    size: SizeType
    stock: int

    model_config = ConfigDict(from_attributes=True)

class ProductVariantRead(BaseModel):
    id: int
    product_id: int
    color: str
    sizes: List[VariantSizeRead]
    imagenes: List[ReadImage]

    model_config = ConfigDict(from_attributes=True)

class ProductRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    marca: BrandType
    categoria: CategoryType
    model_family: str  # Ej: "jean", "drill"
    fit: str | None
    slug: str | None

    variants: List[ProductVariantRead]

    model_config = ConfigDict(from_attributes=True)

class GridProductVariantRead(BaseModel):
    id: int
    imagenes: List[ReadImage]

    model_config = ConfigDict(from_attributes=True)

class GridProductRead(BaseModel):
    id: int
    nombre: str
    categoria: CategoryType   # Ej: "pantalon", "camisa"
    model_family: str | None  # Ej: "jean", "drill"
    slug: str | None

    variants: List[GridProductVariantRead]

    model_config = ConfigDict(from_attributes=True)

class CreateVariantSizeSchema(BaseModel):
    size: SizeType

class CreateProductVariantSchema(BaseModel):
    color: str = Field(max_length=16, min_length=2)
    sizes: List[CreateVariantSizeSchema] = Field(min_length=1)

    temp_key: str

class CreateProductSchema(BaseModel):
    nombre: str = Field(max_length=55)
    descripcion: str 
    marca: BrandType
    categoria: CategoryType 
    model_family: str = Field(min_length=2)
    fit: str | None = Field(None, min_length=2)

    variants: List[CreateProductVariantSchema] = Field(min_length=1, max_length=5)

    temp_keys: List[str] = Field(min_length=1, max_length=40)

class UpdateVariantSizeSchema(BaseModel):
    id: int | None = None
    variant_id: int | None = None
    size: SizeType | None = None

    to_delete: bool = False

class UpdateProductVariantSchema(BaseModel):
    id: int | None = None
    product_id: int | None = None
    color: str | None = Field(default=None, min_length=2, max_length=16, examples=[None])
    sizes: List[UpdateVariantSizeSchema] | None = Field(default=None, min_length=1, examples=[None])
    imagenes: List[UpdateImage] | None = Field(default_factory=[])
    temp_key: str | None = Field(default=None, min_length=2)

    # flags
    to_delete: bool = False

class UpdateProductSchema(BaseModel):
    id: int | None = None
    nombre: str | None = Field(default=None, min_length=8, max_length=55, examples=[None])
    descripcion: str | None = Field(default=None, examples=[None], min_length=2)
    marca: BrandType | None = Field(default=None, examples=[None], min_length=2)
    categoria: CategoryType | None = Field(default=None, min_length=4, examples=[None]) # Ej: "pantalon", "camisa"
    model_family: str | None = Field(default=None, min_length=2)
    fit: str | None = Field(default=None, examples=[None], min_length=2)  # Ej: "jean", "drill"

    variants: List[UpdateProductVariantSchema] | None = Field(default=None, min_length=1, max_length=5)
    temp_keys: List[str] | None = Field(default=None)

    # flags
    name_changed: bool = False

class FilterSchema(BaseModel):
    name: str | None = None
    marca: BrandType | None = None
    categoria: CategoryType | None = None
    model_family: str | None = None
    color: ColorFilter | None = None
    sizes: List[SizeType] | None = None
    sku: str | None = None
    
class GetGridProductsResponse(BaseModel):
    pagination: PaginationResponseSchema
    products: List[GridProductRead]
    total_items: int

class CreateProductResponse(BaseModel):
    id: int
    slug: str

    model_config = ConfigDict(from_attributes=True)