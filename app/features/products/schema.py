from pydantic import BaseModel, Field, ConfigDict
from typing import List

from app.features.media.schema import ReadImage
from app.shared.pagination.schema import PaginationResponseSchema
from app.features.products.types import ColorFilter, BrandType, CategoryType, SizeType, FitType
from app.features.inventory.schemas.inventory_schema import CreateInventorySchema

class VariantSizeRead(BaseModel):
    id: int
    variant_id: int
    size: SizeType
    sku: str | None
    barcode: str | None

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
    brand: BrandType
    category: CategoryType
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
    category: CategoryType   # Ej: "pantalon", "camisa"
    brand: BrandType
    fit: FitType
    slug: str | None

    variants: List[GridProductVariantRead]

    model_config = ConfigDict(from_attributes=True)


class CreateVariantSizeSchema(BaseModel):
    size: SizeType

    inventories: List[CreateInventorySchema] = Field(
        default_factory=list,
    )

    barcode: str | None = None


class CreateProductVariantSchema(BaseModel):
    color: str = Field(
        min_length=2,
        max_length=16,
    )

    sizes: List[CreateVariantSizeSchema] = Field(
        min_length=1,
    )

    temp_key: str


class CreateProductSchema(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=255,
    )

    descripcion: str

    category: CategoryType

    brand: BrandType

    fit: str

    variants: List[CreateProductVariantSchema] = Field(
        min_length=1,
    )

    temp_keys: List[str]

class UpdateProductSchema(BaseModel):
    id: int | None = None
    nombre: str | None = Field(default=None, min_length=8, max_length=55, examples=[None])
    descripcion: str | None = Field(default=None, examples=[None], min_length=2)
    brand: BrandType | None = Field(default=None, examples=[None], min_length=2)
    category: CategoryType | None = Field(default=None, min_length=4, examples=[None]) # Ej: "pantalon", "camisa"\
    fit: str | None = Field(default=None, examples=[None], min_length=2)  # Ej: "jean", "drill"

    # flags
    name_changed: bool = False

class FilterSchema(BaseModel):
    name: str | None = None
    brand: BrandType | None = None
    category: CategoryType | None = None
    color: ColorFilter | None = None
    sizes: List[SizeType] | None = None
    sku: str | None = None
    
class GetGridProductsResponse(BaseModel):
    pagination: PaginationResponseSchema
    items: List[GridProductRead]
    total_items: int

    model_config = ConfigDict(from_attributes=True)

class CreateProductResponse(BaseModel):
    id: int
    slug: str

    model_config = ConfigDict(from_attributes=True)