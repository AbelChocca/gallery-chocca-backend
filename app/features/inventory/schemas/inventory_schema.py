from decimal import Decimal
from pydantic import BaseModel, Field

class UpdateInventoryLocationSchema(BaseModel):
    location_id: int

    minimum_stock: Decimal = Field(
        ge=0,
    )

class CreateInventorySchema(BaseModel):
    location_id: int

    minimum_stock: Decimal = Field(ge=0)

    initial_stock: Decimal | None = Field(
        default=None,
        ge=0,
    )