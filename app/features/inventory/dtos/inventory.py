from app.features.inventory.types.inventory import AvailabilityStatus
from app.features.inventory.dtos.inventory_locations import InventoryLocationStockDTO
from app.features.material.dto.material_component import MaterialComponentDTO
from app.shared.types import CompanyType

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass
class ProductInventoryDetailDTO:
    variant_size_id: int
    variant_id: int

    name: str

    color: str
    size: str

    sku: str
    barcode: str | None

    image_url: str | None

    total_quantity: Decimal
    total_reserved_quantity: Decimal
    total_available_quantity: Decimal

    total_minimum_stock: Decimal

    availability_status: AvailabilityStatus

    locations: list[InventoryLocationStockDTO]

@dataclass(slots=True)
class ProductInventoryRowDTO:
    variant_size_id: int
    variant_id: int

    name: str

    color: str
    size: str

    sku: str
    barcode: str | None

    image_url: str | None

    available_quantity: Decimal
    total_quantity: Decimal
    total_minimum_stock: Decimal
    reserved_quantity: Decimal

    availability_status: AvailabilityStatus

    has_stock_in_other_locations: bool

    other_locations_total_quantity: Decimal

@dataclass(slots=True)
class MaterialInventoryDetailDTO:

    material_id: int

    code: str
    name: str

    description: str | None

    company: CompanyType
    material_type: str
    unit_type: str

    image_url: str | None

    total_quantity: Decimal
    total_reserved_quantity: Decimal
    total_available_quantity: Decimal

    minimum_stock: Decimal

    availability_status: AvailabilityStatus

    is_active: bool

    created_at: datetime
    updated_at: datetime

    components: list[MaterialComponentDTO]

    locations: list[InventoryLocationStockDTO]

@dataclass(slots=True)
class MaterialInventoryRowDTO:
    material_id: int

    code: str
    name: str

    material_type: str
    unit_type: str

    image_url: str | None

    available_quantity: Decimal
    total_quantity: Decimal
    reserved_quantity: Decimal
    minimum_stock: Decimal

    availability_status: AvailabilityStatus

    is_active: bool

@dataclass
class CreateInventoryCommand:
    location_id: int
    minimum_stock: Decimal
    initial_stock: Decimal | None = None

@dataclass(slots=True)
class UpdateInventoryLocationDTO:
    location_id: int

    minimum_stock: Decimal

@dataclass
class InventoryStockUpdateResult:
    owner_id: int
    location_id: int

    previous_stock: Decimal
    current_stock: Decimal