from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.features.pricing.schemas.promotion_schema import (
    AppliedPromotionResponseSchema,
)
from app.features.payments.types.payment import (
    PaymentMethod,
)
from app.features.orders.types.delivery import DeliveryMethod

class ShippingLocationRequest(BaseModel):
    address: str
    latitude: Decimal
    longitude: Decimal
    ubigeo_code: str


class CheckoutPreviewRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    delivery_method: DeliveryMethod = DeliveryMethod.SHIPPING

    shipping_location: ShippingLocationRequest | None = None

    pickup_location_id: int | None = Field(default=None, gt=0)


    coupon_code: str | None = Field(
        default=None,
        max_length=100,
    )

    payment_method: PaymentMethod | None = None

    @model_validator(mode="after")
    def validate_delivery(self):
        if self.delivery_method == DeliveryMethod.SHIPPING:
            if self.pickup_location_id is not None:
                raise ValueError(
                    "SHIPPING no permite pickup_location_id."
                )

        elif self.delivery_method == DeliveryMethod.STORE_PICKUP:
            if self.pickup_location_id is None:
                raise ValueError(
                    "STORE_PICKUP requiere pickup_location_id."
                )

            if self.shipping_location is not None:
                raise ValueError(
                    "STORE_PICKUP no permite shipping_location."
                )

        return self


class CheckoutItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    product_id: int
    name: str

    variant_id: int
    color: str

    variant_size_id: int
    size: str
    sku: str

    quantity: int
    image_url: str | None

    original_price: Decimal
    final_price: Decimal

    original_total: Decimal
    discount_amount: Decimal
    final_total: Decimal

    applied_promotions: list[
        AppliedPromotionResponseSchema
    ]

class CheckoutPreviewResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    cart_id: int

    items: list[CheckoutItemResponse]

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    total_items: int

    applied_promotions: list[
        AppliedPromotionResponseSchema
    ]

