from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class ShippingLocationDTO:
    address: str
    latitude: Decimal
    longitude: Decimal
    ubigeo_code: str