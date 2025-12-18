from dataclasses import dataclass
from typing import Optional

@dataclass
class ReadVariantImageDTO:
    id: int
    variant_id: int
    url: str
    cloudinary_id: str

@dataclass
class UpdateVariantImageDTO:
    id: Optional[int] = None
    variant_id: Optional[int] = None
    url: Optional[str] = None
    cloudinary_id: Optional[str] = None

    # flags
    to_delete: bool = False