from dataclasses import dataclass
from typing import List, Optional

@dataclass
class VariantImageDTO:
    url: str
    cloudinary_id: str

@dataclass
class ColorVariantDTO:
    color: str
    tallas: List[str]
    imagenes: List[VariantImageDTO]

@dataclass
class UpdateVariantImageDTO:
    id: Optional[int] = None
    variant_id: Optional[int] = None
    url: Optional[str] = None
    cloudinary_id: Optional[str] = None

@dataclass
class UpdateProductColorVariantDTO:
    id: Optional[int] = None
    product_id: Optional[int] = None
    color: Optional[str] = None
    tallas: Optional[List[str]] = None
    imagenes: Optional[List[UpdateVariantImageDTO]] = None