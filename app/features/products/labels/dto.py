from decimal import Decimal
from dataclasses import dataclass
from app.features.products.types import BrandType

@dataclass(slots=True)
class LabelRequest:
    variant_size_id: int
    quantity: int

@dataclass
class LabelDTO:

    product_name: str

    barcode: str

    brand_type: BrandType

    variant_size_id: int | None = None
    
    base_price: Decimal | None = None