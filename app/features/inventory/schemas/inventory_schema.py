from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.features.inventory.types.inventory import InventoryAnalysisStatus
from app.features.inventory.types.inventory_movement import InventoryOwnerType
from app.features.material.types import UnitType

class UpdateInventoryLocationSchema(BaseModel):
    location_id: int

    minimum_stock: Decimal = Field(
        ge=0,
    )

    unit_price: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
    )

class CreateInventorySchema(BaseModel):
    location_id: int

    minimum_stock: Decimal = Field(ge=0)

    initial_stock: Decimal | None = Field(
        default=None,
        ge=0,
    )

    unit_price: Decimal = Field(
        default=Decimal("0"),
        ge=0
    )

    @field_validator("initial_stock", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None

        return value

class InventoryAnalysisRequest(BaseModel):
    owner_type: InventoryOwnerType
    owner_id: int

class InventoryAnalysisResponse(BaseModel):

    model_config = ConfigDict(
            from_attributes=True
        )

    status: InventoryAnalysisStatus
    consumption_7d: Decimal
    consumption_30d: Decimal

    coverage_days: Decimal | None

class InventoryKPIsResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    
    inventory_value: Decimal

    total_items: int
    items_below_minimum: int

    reserved_items: int
    reserved_quantity: Decimal

    items_without_movement: int

    total_entries: Decimal
    total_exits: Decimal

class InventoryKPIsRequest(BaseModel):
    owner_type: InventoryOwnerType
    current_location_id: int

class InventoryConsumptionPointResponse(BaseModel):
    date: date
    quantity: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )

class InventoryConsumptionChartRequest(BaseModel):
    owner_type: InventoryOwnerType
    owner_id: int
    current_location_id: int
    days: int = 30
    
class InventoryConsumptionChartResponse(BaseModel):
    unit_type: UnitType
    points: list[InventoryConsumptionPointResponse]

    model_config = ConfigDict(
        from_attributes=True
    )