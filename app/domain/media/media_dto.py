from dataclasses import dataclass
from typing import Optional

@dataclass
class MediaImageDTO:
    url: str
    public_id: str

@dataclass
class ReadMediaImageDTO:
    image_url: str
    owner_type: str
    service_id: str
    owner_id: Optional[int] = None
    id: Optional[int] = None
    alt_text: Optional[str] = None

@dataclass
class UpdateImageDTO:
    id: Optional[int] = None
    owner_id: Optional[int] = None
    image_url: Optional[str] = None
    service_id: Optional[str] = None

    # flags
    to_delete: bool = False