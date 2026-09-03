from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationCategory,
    InventoryValuationSubcategory,
)
from app.shared.types import CompanyType

@dataclass
class InventoryValuation:
    balance_snapshot_id: int
    category: InventoryValuationCategory
    subcategory: InventoryValuationSubcategory | None
    description: str
    brand: CompanyType | None
    location: str | None
    quantity: Decimal
    unit_value: Decimal

    id: int | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None


    @property
    def total_value(self) -> Decimal:
        return self.quantity * self.unit_value