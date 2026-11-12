
from pydantic import BaseModel, ConfigDict


class UbigeoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    department: str
    province: str
    district: str
    city_name: str | None
