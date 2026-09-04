from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.features.balancing.types.other_current_liability_types import OtherCurrentLiabilityCategory, OtherCurrentLiabilityStatus   


class OtherCurrentLiabilityUpdateSchema(BaseModel):

    category: OtherCurrentLiabilityCategory | None = None
    description: str | None = None
    amount: Decimal | None = None
    status: OtherCurrentLiabilityStatus | None = None

class OtherCurrentLiabilityCreateSchema(BaseModel):

    balance_snapshot_id: int
    category: OtherCurrentLiabilityCategory
    description: str
    amount: Decimal
    status: OtherCurrentLiabilityStatus


class OtherCurrentLiabilityFilterSchema(BaseModel):

    balance_snapshot_id: int | None = None
    category: OtherCurrentLiabilityCategory | None = None
    status: OtherCurrentLiabilityStatus | None = None


class OtherCurrentLiabilityResponseSchema(BaseModel):

    id: int
    balance_snapshot_id: int
    category: OtherCurrentLiabilityCategory
    description: str
    amount: Decimal
    status: OtherCurrentLiabilityStatus
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)