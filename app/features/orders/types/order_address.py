from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class AdminOrderAddressDTO:
    recipient_name: str
    phone: str

    ubigeo_code: str

    department: str
    province: str
    district: str
    city_name: str | None

    address: str

    latitude: Decimal
    longitude: Decimal

    reference: str | None
    delivery_instructions: str | None

@dataclass(frozen=True, slots=True)
class MyOrderAddressDTO:
    recipient_name: str
    phone: str

    ubigeo_code: str

    department: str
    province: str
    district: str
    city_name: str | None

    address: str

    latitude: Decimal
    longitude: Decimal

    reference: str | None

    delivery_instructions: str | None