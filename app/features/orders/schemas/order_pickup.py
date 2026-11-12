from pydantic import BaseModel, ConfigDict


class OrderPickupDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    location_id: int
    name: str
    address: str