from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ubigeo:
    code: str
    department: str
    province: str
    district: str
    city_name: str | None