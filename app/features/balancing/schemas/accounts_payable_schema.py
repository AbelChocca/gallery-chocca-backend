from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.features.balancing.types.accounts_payable_types import AccountsPayableCostCenter, AccountsPayableStatus
from decimal import Decimal

class AccountsPayableCreateSchema(BaseModel):
    
    balance_snapshot_id: int
    brand: str
    entity_name: str
    cost_center: AccountsPayableCostCenter | None = None
    amount: Decimal
    status: AccountsPayableStatus


class AccountsPayableFilterSchema(BaseModel):

    balance_snapshot_id: int | None = None
    brand: str | None = None
    cost_center: AccountsPayableCostCenter | None = None
    status: AccountsPayableStatus | None = None


class AccountsPayableResponseSchema(BaseModel):

    id: int
    balance_snapshot_id: int
    brand: str
    entity_name: str
    cost_center: AccountsPayableCostCenter | None
    amount: Decimal
    status: AccountsPayableStatus
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AccountsPayableUpdateSchema(BaseModel):

    brand: str | None = None
    entity_name: str | None = None
    cost_center: AccountsPayableCostCenter | None = None
    amount: Decimal | None = None
    status: AccountsPayableStatus | None = None

    