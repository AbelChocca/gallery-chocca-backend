from dataclasses import dataclass


@dataclass(slots=True)
class DeliveryRequest:
    recipient_name: str

    recipient_phone: str

    department: str

    province: str

    district: str

    address: str

    reference: str | None