from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.features.balancing.types.financial_debt_types import FinancialDebtStatus

class FinancialDebtUpdateSchema(BaseModel):

    bank_name: str | None = None
    amount: Decimal | None = None
    status: FinancialDebtStatus | None = None

class FinancialDebtCreateSchema(BaseModel):

    balance_snapshot_id: int
    bank_name: str
    amount: Decimal
    status: FinancialDebtStatus


class FinancialDebtFilterSchema(BaseModel):

    balance_snapshot_id: int | None = None
    bank_name: str | None = None
    fiscal_year: int | None = None
    status: FinancialDebtStatus | None = None


class FinancialDebtResponseSchema(BaseModel):

    id: int
    balance_snapshot_id: int
    bank_name: str
    amount: Decimal
    status: FinancialDebtStatus
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)