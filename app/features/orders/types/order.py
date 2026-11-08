from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from decimal import Decimal

from app.features.pricing.dtos.cart_pricing_dto import (
    AppliedPromotionDTO,
)

from app.features.customer.customer_types import IdentityDocumentType
from app.features.receipts.types.document import BillingDocumentType
from app.features.orders.types.order_address import AdminOrderAddressDTO, MyOrderAddressDTO
from app.features.orders.types.order_billing import AdminOrderBillingDTO, MyOrderBillingDTO
from app.features.orders.types.order_item import AdminOrderItemDTO, MyOrderItemDTO
from app.features.orders.types.order_promotion import AdminOrderPromotionDTO, MyOrderPromotionDTO
from app.features.customer.dtos.customer import AdminOrderCustomerDTO, MyOrderCustomerDTO
from app.features.orders.types.order_receipt import AdminOrderReceiptDTO 
from app.features.orders.types.order_pickup import OrderPickupDetailDTO   

from app.features.payments.types.payment import (
    PaymentMethod,
)
from app.features.orders.types.delivery import DeliveryMethod

class OrderStatus(str, Enum):
    PENDING_SHIPPING_QUOTE = "PENDING_SHIPPING_QUOTE"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

@dataclass(slots=True)
class CheckoutItemDTO:
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

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )


@dataclass(slots=True)
class CheckoutPreviewDTO:
    cart_id: int
    items: list[CheckoutItemDTO]

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    total_items: int

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )

@dataclass(frozen=True, slots=True)
class CreateOrderCustomerDTO:
    name: str
    last_name: str
    email: str
    phone: str


@dataclass(frozen=True, slots=True)
class CreateOrderAddressDTO:
    recipient_name: str
    phone: str
    address: str
    latitude: Decimal
    longitude: Decimal
    ubigeo_code: str
    reference: str | None = None
    delivery_instructions: str | None = None


@dataclass(frozen=True, slots=True)
class CreateOrderBillingDTO:
    document_type: BillingDocumentType
    document_number_type: IdentityDocumentType
    document_number: str
    legal_name: str | None = None
    billing_address: str | None = None

@dataclass(frozen=True, slots=True)
class CreateOrderBillingDTO:
    document_type: BillingDocumentType
    identity_document_number: str

    business_name: str | None = None
    billing_address: str | None = None

@dataclass
class CreateOrderPickupDTO:
    location_id: int

@dataclass(frozen=True, slots=True)
class CreateOrderInput:
    user_id: int | None
    session_id: str | None

    customer: CreateOrderCustomerDTO | None

    delivery_method: DeliveryMethod
    address: CreateOrderAddressDTO | None
    pickup: CreateOrderPickupDTO | None

    billing: CreateOrderBillingDTO | None

    coupon_code: str | None = None
    payment_method: PaymentMethod | None = None

@dataclass(frozen=True, slots=True)
class CreateOrderItemResult:
    product_name: str
    color: str | None
    size: str | None
    quantity: int
    final_total: Decimal

@dataclass(frozen=True, slots=True)
class CreateOrderResult:
    id: int
    order_number: str
    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    items: list[CreateOrderItemResult]


@dataclass(frozen=True, slots=True)
class GetMyOrderItemResult:
    product_name: str
    color: str | None
    size: str | None
    quantity: int
    final_total: Decimal


@dataclass(frozen=True, slots=True)
class GetMyOrderResult:
    id: int
    order_number: str
    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    items: list[GetMyOrderItemResult]

@dataclass(frozen=True, slots=True)
class AdminOrderListItemDTO:
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

@dataclass(frozen=True, slots=True)
class OrderFilters:
    search: str | None = None
    status: OrderStatus | None = None

    created_at_from: datetime | None = None
    created_at_to: datetime | None = None

@dataclass(frozen=True, slots=True)
class AdminOrderDetailDTO:
    id: int
    order_number: str

    status: OrderStatus

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    customer: AdminOrderCustomerDTO

    items: list[AdminOrderItemDTO]

    promotions: list[AdminOrderPromotionDTO]

    delivery_method: DeliveryMethod

    address: AdminOrderAddressDTO | None
    pickup: OrderPickupDetailDTO | None

    billing: AdminOrderBillingDTO | None

    receipt: AdminOrderReceiptDTO | None

    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True, slots=True)
class UpdateOrderShippingDTO:
    shipping_cost: Decimal

@dataclass(frozen=True, slots=True)
class UpdateOrderShippingResult:
    id: int
    order_number: str

    status: OrderStatus

    shipping_cost: Decimal
    total: Decimal

@dataclass(frozen=True, slots=True)
class MyOrderDetailDTO:
    id: int

    order_number: str

    status: OrderStatus

    payment_method: PaymentMethod

    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    total: Decimal

    customer: MyOrderCustomerDTO

    items: list[MyOrderItemDTO]

    promotions: list[MyOrderPromotionDTO]

    delivery_method: DeliveryMethod

    address: MyOrderAddressDTO | None
    pickup: OrderPickupDetailDTO | None

    billing: MyOrderBillingDTO | None

    created_at: datetime
    updated_at: datetime