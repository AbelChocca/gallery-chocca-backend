from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime

class InventoryMovementType(Enum):
    RESTOCK = "restock"
    MANUAL_ADJUSTMENT = "manual_adjustment"
    SALE = "sale"
    RETURN = "return"

@dataclass
class CreateMovementCommand:
    variant_size_id: int
    product_id: int
    type: InventoryMovementType
    quantity: int
    reason: str | None = None

@dataclass
class InventoryMovementFilters:
    from_date: datetime | None = None
    to_date: datetime | None = None
    sku: str | None = None
    type: InventoryMovementType | None = None

    @property
    def to_dict(self) -> dict:
        return asdict(self)