from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableStatus,
)
from app.shared.types import CompanyType


class AccountsReceivableFilters(BaseModel):
    balance_snapshot_id: int | None = None
    brand: str | None = None
    entity_name: str | None = None
    location: str | None = None
    status: AccountsReceivableStatus | None = None

class AccountsReceivableCreateSchema(BaseModel):
    balance_snapshot_id: int
    brand: CompanyType
    entity_name: str
    location: str
    amount: Decimal
    status: AccountsReceivableStatus


class AccountsReceivableUpdateSchema(BaseModel):
    brand: CompanyType | None = None
    entity_name: str | None = None
    location: str | None = None
    amount: Decimal | None = None
    status: AccountsReceivableStatus | None = None


class AccountsReceivableResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    balance_snapshot_id: int
    brand: CompanyType
    entity_name: str
    location: str | None
    amount: Decimal
    status: AccountsReceivableStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)