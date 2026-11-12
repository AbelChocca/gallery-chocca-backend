from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderAddress:
    order_id: int

    recipient_name: str
    phone: str

    ubigeo_code: str

    address: str

    latitude: Decimal
    longitude: Decimal

    id: int | None = None
    reference: str | None = None
    delivery_instructions: str | None = None