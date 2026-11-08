
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.locations.types import LocationType


@dataclass
class Location:
    name: str
    type: LocationType

    address: str | None = None
    ubigeo_code: str | None = None

    latitude: Decimal | None = None
    longitude: Decimal | None = None

    phone: str | None = None
    reference: str | None = None

    external_provider: str | None = None
    external_code: str | None = None

    is_active: bool = True
    pickup_enabled: bool = False

    created_at: datetime | None = None
    updated_at: datetime | None = None

    id: int | None = None
