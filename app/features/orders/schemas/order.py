from decimal import Decimal
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.features.payments.types.payment_legacy import PaymentMethod
from app.features.receipts.types.document import BillingDocumentType
from app.features.orders.types.order import OrderStatus
from app.features.orders.types.delivery import DeliveryMethod

from app.features.orders.schemas.order_promotion import AdminOrderPromotionResponseSchema, MyOrderPromotionResponseSchema
from app.features.orders.schemas.order_item import AdminOrderItemResponseSchema, MyOrderItemResponseSchema
from app.features.orders.schemas.order_billing import AdminOrderBillingResponseSchema, MyOrderBillingResponseSchema
from app.features.orders.schemas.order_address import AdminOrderAddressResponseSchema, MyOrderAddressResponseSchema
from app.features.customer.schemas.customer import AdminOrderCustomerResponseSchema, MyOrderCustomerResponseSchema
from app.features.orders.schemas.order_receipt import AdminOrderReceiptResponse
from app.features.orders.schemas.order_pickup import OrderPickupDetailResponse


class CreateCustomerRequestSchema(BaseModel):
    name: str
    last_name: str
    email: str
    phone: str


class OrderAddressRequestSchema(BaseModel):
    recipient_name: str
    phone: str

    ubigeo_code: str

    address: str
    latitude: Decimal
    longitude: Decimal

    reference: str | None = None
    delivery_instructions: str | None = None


class OrderBillingRequestSchema(BaseModel):
    document_type: BillingDocumentType
    identity_document_number: str

    business_name: str | None = None
    billing_address: str | None = None

class OrderPickupRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    location_id: int = Field(gt=0)


class CreateOrderRequestSchema(BaseModel):
    customer: CreateCustomerRequestSchema | None = None

    delivery_method: DeliveryMethod

    address: OrderAddressRequestSchema | None = None
    pickup: OrderPickupRequestSchema | None = None

    billing: OrderBillingRequestSchema | None = None

    coupon_code: str | None = None
    payment_method: PaymentMethod | None = None

    @model_validator(mode="after")
    def validate_delivery(self):
        if self.delivery_method == DeliveryMethod.SHIPPING:
            if self.address is None or self.pickup is not None:
                raise ValueError(
                    "SHIPPING requiere address y no permite pickup."
                )

        elif self.delivery_method == DeliveryMethod.STORE_PICKUP:
            if self.pickup is None or self.address is not None:
                raise ValueError(
                    "STORE_PICKUP requiere pickup y no permite address."
                )

        return self

class CreateOrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_name: str
    color: str | None
    size: str | None
    quantity: int
    final_total: Decimal

class CreateOrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    items: list[CreateOrderItemResponseSchema]

class GetMyOrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    product_name: str
    color: str | None
    size: str | None
    quantity: int
    final_total: Decimal


class GetMyOrderResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    order_number: str
    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    items: list[
        GetMyOrderItemResponseSchema
    ]

class AdminOrderListItemResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    order_number: str

    customer_id: int
    customer_name: str

    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    created_at: datetime

class AdminOrderFiltersSchema(BaseModel):
    search: str | None = None
    status: OrderStatus | None = None

    created_at_from: date | None = None
    created_at_to: date | None = None

class AdminOrderDetailResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    order_number: str

    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    customer: AdminOrderCustomerResponseSchema

    items: list[AdminOrderItemResponseSchema]

    promotions: list[
        AdminOrderPromotionResponseSchema
    ]

    delivery_method: DeliveryMethod

    address: AdminOrderAddressResponseSchema | None
    pickup: OrderPickupDetailResponse | None

    billing: (
        AdminOrderBillingResponseSchema
        | None
    )
    receipt: AdminOrderReceiptResponse | None

    created_at: datetime
    updated_at: datetime

class UpdateOrderShippingRequestSchema(BaseModel):
    shipping_cost: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
    )


class UpdateOrderShippingResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    order_number: str

    status: OrderStatus

    shipping_cost: Decimal
    total: Decimal

class MyOrderDetailResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    order_number: str

    payment_method: PaymentMethod

    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    customer: MyOrderCustomerResponseSchema

    items: list[
        MyOrderItemResponseSchema
    ]

    promotions: list[
        MyOrderPromotionResponseSchema
    ]

    delivery_method: DeliveryMethod

    address: MyOrderAddressResponseSchema | None
    pickup: OrderPickupDetailResponse | None

    billing: (
        MyOrderBillingResponseSchema
        | None
    )

    created_at: datetime
    updated_at: datetime