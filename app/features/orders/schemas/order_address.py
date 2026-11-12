from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class AdminOrderAddressResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

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

class MyOrderAddressResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

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