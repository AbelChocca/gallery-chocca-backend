from sqlmodel import SQLModel, Field
from typing import Optional

class MediaImageTable(SQLModel, table=True):
    __tablename__ = "image"
    id: Optional[int] = Field(default=None, primary_key=True)
    service_id: int = Field(nullable=False)

    image_url: str = Field(nullable=False)
    alt_text: Optional[str] = Field(default=None)

    owner_type: str = Field(index=True)
    owner_id: int = Field(index=True)