from decimal import Decimal
from pydantic import BaseModel, Field, field_validator

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

    @field_validator("initial_stock", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None

        return value