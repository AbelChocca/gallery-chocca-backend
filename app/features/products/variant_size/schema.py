from pydantic import BaseModel
from app.features.products.types import SizeType

class UpdateVariantSizeSchema(BaseModel):
    id: int | None = None
    variant_id: int | None = None
    size: SizeType | None = None

    to_delete: bool = False