from dataclasses import dataclass
from datetime import datetime

from app.features.inventory.types.inventory_movement import InventoryMovementType, InventoryOwnerType

@dataclass(slots=True, frozen=True)
class GenerateInventoryMovementReportCommand:
    owner_type: InventoryOwnerType

    start_date: datetime
    end_date: datetime

@dataclass(slots=True)
class ReportMetadata:
    title: str
    generated_at: datetime

    start_date: datetime
    end_date: datetime

@dataclass(frozen=True)
class ColumnDefinition:
    header: str
    width: int

@dataclass(slots=True)
class InventoryMovementReportRow:
    movement_date: datetime

    owner_code: str
    owner_name: str

    movement_type: InventoryMovementType
    movement_reason: str

    previous_stock: int
    quantity: int
    new_stock: int

@dataclass(slots=True)
class InventoryOwnerSummaryRow:
    owner_id: int
    owner_name: str

    total_entries: int
    total_sales: int

    total_customer_returns: int
    total_supplier_returns: int

    manual_adjustment_increase: int
    manual_adjustment_decrease: int

    final_stock: int

@dataclass(slots=True)
class InventoryReportMetrics:
    total_movements: int

    total_entries: int
    total_sales: int

    total_customer_returns: int
    total_supplier_returns: int

    total_manual_adjustment_increase: int
    total_manual_adjustment_decrease: int

    affected_owners: int

@dataclass(slots=True)
class InventoryMovementReportData:
    metadata: ReportMetadata

    movements: list[InventoryMovementReportRow]
    material_summaries: list[InventoryOwnerSummaryRow]

    metrics: InventoryReportMetrics