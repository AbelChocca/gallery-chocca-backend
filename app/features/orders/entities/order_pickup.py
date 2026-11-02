from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class OrderPickup:
    order_id: int
    location_id: int

    location_name: str
    location_address: str
    location_ubigeo_code: str

    location_latitude: Decimal | None = None
    location_longitude: Decimal | None = None
    location_phone: str | None = None
    location_reference: str | None = None

    created_at: datetime | None = None
    id: int | None = None
