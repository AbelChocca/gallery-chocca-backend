from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, model_validator, ConfigDict

from app.features.balancing.types.balance_snapshot_types import (
    BalanceSnapshotStatus,
)


class BalanceSnapshotCreateSchema(BaseModel):
    period_start: date
    period_end: date
    status: BalanceSnapshotStatus = BalanceSnapshotStatus.DRAFT

    @model_validator(mode="after")
    def validate_period(self):
        if self.period_end < self.period_start:
            raise ValueError(
                "period_end must be greater than or equal to period_start"
            )

        return self


class BalanceSnapshotUpdateSchema(BaseModel):
    period_start: date | None = None
    period_end: date | None = None
    status: BalanceSnapshotStatus | None = None

    @model_validator(mode="after")
    def validate_period(self):
        if (
            self.period_start is not None
            and self.period_end is not None
            and self.period_end < self.period_start
        ):
            raise ValueError(
                "period_end must be greater than or equal to period_start"
            )

        return self


class BalanceSnapshotFilterSchema(BaseModel):
    period_start: date | None = None
    period_end: date | None = None
    status: BalanceSnapshotStatus | None = None


class BalanceResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class BalanceSnapshotResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    period_start: date
    period_end: date
    status: BalanceSnapshotStatus
    created_at: datetime


class BalanceComparisonResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_snapshot_id: int
    previous_snapshot_id: int

    current_period_start: date
    current_period_end: date

    previous_period_start: date
    previous_period_end: date

    current_assets: Decimal
    previous_assets: Decimal
    assets_variation: Decimal

    liabilities: Decimal
    previous_liabilities: Decimal
    liabilities_variation: Decimal

    working_capital: Decimal
    previous_working_capital: Decimal
    working_capital_variation: Decimal