from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderPickupDetailDTO:
    location_id: int
    name: str
    address: str