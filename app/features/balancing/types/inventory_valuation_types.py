from enum import StrEnum
from dataclasses import dataclass, field
from decimal import Decimal
from app.shared.types import CompanyType

class InventoryValuationCategory(StrEnum):
    RAW_MATERIAL = "raw_material"
    WORK_IN_PROGRESS = "work_in_progress"
    FINISHED_GOODS = "finished_goods"


class InventoryValuationSubcategory(StrEnum):
    CUTTING = "cutting"
    SEWING = "sewing"
    LAUNDRY = "laundry"
    WAREHOUSE = "warehouse"
    STORE = "store"
    SELLER = "seller"

@dataclass
class InventoryValuationUpdate:

    category: InventoryValuationCategory | None = None
    subcategory: InventoryValuationSubcategory | None = None
    description: str | None = None
    brand: CompanyType | None = None
    location: str | None = None
    quantity: Decimal | None = None
    unit_value: Decimal | None = None

    fields_set: set[str] = field(default_factory=set)

@dataclass(slots=True)
class InventoryValuationAnalysisResponse:

    total_amount: Decimal

    raw_material_amount: Decimal

    work_in_progress_amount: Decimal

    finished_goods_amount: Decimal