from pydantic import BaseModel, Field, ConfigDict
from app.domain.inventory.data_models import InventoryMovementType
from app.domain.product.dto.product_dto import CategoryType, BrandType
from app.api.schemas.media.media_schema import ReadImage
from app.api.schemas.pagination import PaginationResponseSchema
from datetime import datetime

class CreateMovementSchema(BaseModel):
    product_id: int
    variant_size_id: int 
    type: InventoryMovementType
    quantity: int
    reason: str | None = Field(default=None, max_length=255)

class InventoryVariantSizeRead(BaseModel):
    id: int
    size: str
    stock: int
    sku: str

    model_config = ConfigDict(from_attributes=True)

class InventoryProductVariantRead(BaseModel):
    id: int
    color: str
    sizes: list[InventoryVariantSizeRead]
    imagen: ReadImage

    model_config = ConfigDict(from_attributes=True)

class InventoryProductRead(BaseModel):
    id: int
    nombre: str
    categoria: CategoryType
    model_family: str | None = None  # Ej: "jean", "drill"
    fit: str | None = None
    marca: BrandType

    variants: list[InventoryProductVariantRead]

    model_config = ConfigDict(from_attributes=True)

class InventoryMovementRead(BaseModel):
    variant_size_id: int
    type: InventoryMovementType
    quantity: int
    previous_stock: int
    new_stock: int
    reason: str
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class InventoryMovementFilterSchema(BaseModel):
    from_date: datetime | None = None
    to_date: datetime | None = None
    sku: str | None = None
    type: InventoryMovementType | None = None

class GetInventoryItemsResponse(BaseModel):
    products: list[InventoryProductRead]
    pagination: PaginationResponseSchema
    total_items: int

class GetInventoryMovementsResponse(BaseModel):
    movements: list[InventoryMovementRead]
    pagination: PaginationResponseSchema
    total_items: int