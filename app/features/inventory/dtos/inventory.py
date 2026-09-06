from app.features.inventory.types.inventory import AvailabilityStatus, InventoryAnalysisStatus
from app.features.inventory.dtos.inventory_locations import InventoryLocationStockDTO
from app.features.material.dto.material_component import MaterialComponentDTO
from app.shared.types import CompanyType
from app.features.material.types import UnitType

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, date

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

    days_without_rotation: int | None

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

    unit_price: Decimal | None = Decimal("0")
    

@dataclass(slots=True)
class UpdateInventoryLocationDTO:
    location_id: int

    minimum_stock: Decimal

    unit_price: Decimal | None = None

@dataclass
class InventoryStockUpdateResult:
    owner_id: int
    location_id: int

    previous_stock: Decimal
    current_stock: Decimal

@dataclass
class InventoryAnalysisDTO:
    status: InventoryAnalysisStatus
    consumption_7d: Decimal
    consumption_30d: Decimal

    coverage_days: Decimal | None 


@dataclass(slots=True)
class InventoryKPIsDTO:
    inventory_value: Decimal

    total_items: int
    items_below_minimum: int

    reserved_items: int
    reserved_quantity: Decimal

    items_without_movement: int

    total_entries: Decimal
    total_exits: Decimal

@dataclass(slots=True)
class InventoryKPIItemDTO:
    owner_id: int
    quantity: Decimal
    reserved_quantity: Decimal
    minimum_stock: Decimal
    unit_price: Decimal | None

@dataclass(slots=True)
class InventoryConsumptionPointDTO:
    date: date
    quantity: Decimal

@dataclass(slots=True)
class InventoryConsumptionChartDTO:
    unit_type: UnitType
    points: list[InventoryConsumptionPointDTO]

@dataclass(slots=True)
class InventoryOwnerDTO:
    id: int
    unit_type: UnitType