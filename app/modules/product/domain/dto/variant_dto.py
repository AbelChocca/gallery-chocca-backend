from dataclasses import dataclass
from typing import List, Optional

from app.modules.product.domain.dto.variant_image_dto import ReadVariantImageDTO, UpdateVariantImageDTO

@dataclass
class ReadProductVariantDTO:
    id: int
    product_id: int
    color: str
    tallas: List[str]
    imagenes: List[ReadVariantImageDTO]

@dataclass
class UpdateProductVariantDTO:
    id: Optional[int] = None
    product_id: Optional[int] = None
    color: Optional[str] = None
    tallas: Optional[List[str]] = None
    imagenes: Optional[List[UpdateVariantImageDTO]] = None

    # flags
    to_delete: bool = False