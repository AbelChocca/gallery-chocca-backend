from decimal import Decimal
from pydantic import BaseModel, ConfigDict

from app.features.inventory.schemas.inventory_location_schema import InventoryLocationStockSchema

from app.features.inventory.types.inventory import (
    AvailabilityStatus,
)

class InventoryProductFilterSchema(BaseModel):
    search: str | None = None
    color: str | None = None
    size: str | None = None

    current_location_id: int = 1

class ProductInventoryDetailSchema(BaseModel):
    variant_size_id: int
    variant_id: int

    name: str

    color: str
    size: str

    sku: str
    barcode: str | None = None

    image_url: str | None = None

    total_quantity: Decimal
    total_reserved_quantity: Decimal
    total_available_quantity: Decimal

    total_minimum_stock: Decimal

    availability_status: AvailabilityStatus

    locations: list[InventoryLocationStockSchema]

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductInventoryRowSchema(BaseModel):
    variant_size_id: int
    variant_id: int

    name: str

    color: str
    size: str

    sku: str
    barcode: str | None = None

    image_url: str | None = None

    available_quantity: Decimal
    total_quantity: Decimal
    total_minimum_stock: Decimal
    reserved_quantity: Decimal

    availability_status: AvailabilityStatus

    has_stock_in_other_locations: bool

    other_locations_total_quantity: Decimal