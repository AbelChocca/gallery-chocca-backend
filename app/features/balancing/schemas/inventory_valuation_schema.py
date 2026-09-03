from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.shared.types import CompanyType
from app.features.balancing.types.inventory_valuation_types import InventoryValuationCategory, InventoryValuationSubcategory


class InventoryValuationUpdateSchema(BaseModel):

    category: InventoryValuationCategory | None = None
    subcategory: InventoryValuationSubcategory | None = None
    description: str | None = None
    brand: CompanyType | None = None
    location: str | None = None
    quantity: Decimal | None = None
    unit_value: Decimal | None = None

class InventoryValuationCreateSchema(BaseModel):

    balance_snapshot_id: int
    category: InventoryValuationCategory
    subcategory: InventoryValuationSubcategory | None = None
    description: str
    brand: CompanyType | None = None
    location: str | None = None
    quantity: Decimal
    unit_value: Decimal


class InventoryValuationFilterSchema(BaseModel):

    balance_snapshot_id: int | None = None
    category: InventoryValuationCategory | None = None
    subcategory: str | None = None
    brand: str | None = None
    location: str | None = None


class InventoryValuationResponseSchema(BaseModel):

    id: int
    balance_snapshot_id: int
    category: InventoryValuationCategory
    subcategory: InventoryValuationSubcategory | None
    description: str
    brand: CompanyType | None
    location: str | None
    quantity: Decimal
    unit_value: Decimal
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)