from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ReadImage(BaseModel):
    image_url: str
    owner_type: str
    service_id: str
    owner_id: Optional[int] = Field(default=None)
    id: Optional[int] = Field(default=None)
    alt_text: Optional[str] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

class UpdateImage(BaseModel):
    id: Optional[int] = Field(default=None)
    owner_id: Optional[int] = Field(default=None)
    image_url: Optional[str] = Field(default=None, examples=[None])
    service_id: Optional[str] = Field(default=None, examples=[None])

    # flags
    to_delete: bool = Field(default=False)