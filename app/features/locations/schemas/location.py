from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.features.locations.types import LocationType


class CreateLocationRequestSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(min_length=2, max_length=150)
    type: LocationType

    address: str | None = Field(default=None, max_length=255)
    ubigeo_code: str | None = Field(
        default=None,
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
    )

    latitude: Decimal | None = Field(
        default=None, ge=-90, le=90
    )
    longitude: Decimal | None = Field(
        default=None, ge=-180, le=180
    )

    phone: str | None = Field(default=None, max_length=30)
    reference: str | None = Field(default=None, max_length=255)

    external_provider: str | None = Field(
        default=None, max_length=50
    )
    external_code: str | None = Field(
        default=None, max_length=100
    )

    is_active: bool = True
    pickup_enabled: bool = False


class LocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

    address: str
    ubigeo_code: str

    latitude: Decimal | None
    longitude: Decimal | None

    phone: str | None
    reference: str | None

class AdminLocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: LocationType

    address: str | None
    ubigeo_code: str | None

    latitude: Decimal | None
    longitude: Decimal | None

    phone: str | None
    reference: str | None

    external_provider: str | None
    external_code: str | None

    is_active: bool
    pickup_enabled: bool

    created_at: datetime | None
    updated_at: datetime | None


class AdminLocationFiltersSchema(BaseModel):
    search: str | None = Field(
        default=None,
        max_length=120,
    )
    type: LocationType | None = None
    is_active: bool | None = None
    pickup_enabled: bool | None = None
