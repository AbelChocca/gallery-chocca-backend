from enum import StrEnum
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import date, datetime


class BalanceSnapshotStatus(StrEnum):
    DRAFT = "draft"
    CLOSED = "closed"
    CANCELLED = "cancelled"

@dataclass
class BalanceSnapshotUpdate:

    period_start: date | None = None
    period_end: date | None = None
    status: BalanceSnapshotStatus | None = None

    fields_set: set[str] = field(default_factory=set)

@dataclass(slots=True)
class BalanceResponse:

    id: int
    
    period_start: date

    period_end: date

    status: BalanceSnapshotStatus

    created_at: datetime

    total_current_assets: Decimal

    total_current_liabilities: Decimal

    working_capital: Decimal

    accounts_receivable: Decimal

    raw_material: Decimal

    work_in_progress: Decimal

    finished_goods: Decimal

    accounts_payable: Decimal

    financial_debt: Decimal

    other_current_liabilities: Decimal

@dataclass(slots=True)
class BalanceSnapshotResponse:

    id: int

    period_start: date

    period_end: date

    status: BalanceSnapshotStatus

    created_at: datetime

@dataclass(slots=True)
class BalanceComparisonResponse:

    current_snapshot_id: int

    previous_snapshot_id: int

    current_period_start: str

    current_period_end: str

    previous_period_start: str

    previous_period_end: str

    current_assets: Decimal

    previous_assets: Decimal

    assets_variation: Decimal

    liabilities: Decimal

    previous_liabilities: Decimal

    liabilities_variation: Decimal

    working_capital: Decimal

    previous_working_capital: Decimal

    working_capital_variation: Decimal