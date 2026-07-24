from pydantic import BaseModel, Field
from app.features.media.schema import UpdateImage
from app.features.products.variant_size.schema import UpdateVariantSizeSchema

class UpdateProductVariantSchema(BaseModel):
    id: int | None = None
    product_id: int | None = None
    color: str | None = Field(default=None, min_length=2, max_length=16, examples=[None])
    sizes: list[UpdateVariantSizeSchema] | None = Field(default=None, min_length=1, examples=[None])
    imagenes: list[UpdateImage] | None = Field(default_factory=[])
    temp_key: str | None = Field(default=None, min_length=2)

    # flags
    to_delete: bool = False