from dataclasses import dataclass
from enum import Enum

class ImageType(str, Enum):
    variant = "variant"
    slide = "slide"

@dataclass
class MediaImageDTO:
    url: str
    public_id: str

@dataclass
class ReadMediaImageDTO:
    image_url: str
    id: int | None = None
    alt_text: int | None = None

@dataclass
class UpdateImageCommand:
    id: int | None = None
    owner_id: int | None = None
    image_url: str | None = None
    public_id: str | None = None

    # flags
    to_delete: bool = False
