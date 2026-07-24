from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.features.inventory.schemas.inventory_location_schema import InventoryLocationStockSchema
from app.features.material.types import MaterialType, UnitType
from app.features.material.schema import MaterialComponentSchema
from app.shared.types import CompanyType

from app.features.inventory.types.inventory import (
    AvailabilityStatus,
)

class MaterialInventoryDetailSchema(BaseModel):

    material_id: int

    code: str
    name: str

    description: str | None

    company: CompanyType
    material_type: MaterialType
    unit_type: UnitType

    image_url: str | None

    total_quantity: Decimal
    total_reserved_quantity: Decimal
    total_available_quantity: Decimal

    minimum_stock: Decimal

    availability_status: AvailabilityStatus

    is_active: bool

    created_at: datetime
    updated_at: datetime

    components: list[MaterialComponentSchema]

    locations: list[InventoryLocationStockSchema]

    model_config = ConfigDict(
        from_attributes=True
    )

class InventoryMaterialFilterSchema(BaseModel):
    search: str | None = Field(
        default=None,
        max_length=100,
    )

    material_type: MaterialType | None = None

    availability_status: AvailabilityStatus | None = None

    is_active: bool | None = None

    current_location_id: int = 1

class MaterialInventoryRowSchema(BaseModel):
    material_id: int

    code: str
    name: str

    material_type: MaterialType
    unit_type: UnitType

    image_url: str | None = None

    available_quantity: Decimal
    total_quantity: Decimal
    reserved_quantity: Decimal
    minimum_stock: Decimal

    availability_status: AvailabilityStatus

    is_active: bool

    model_config = ConfigDict(
            from_attributes=True
        )