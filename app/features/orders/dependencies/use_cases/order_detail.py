from typing import Annotated

from fastapi import Depends

from app.features.customer.customer_service import CustomerService
from app.features.customer.dependencies.services.customer import get_customer_service

from app.features.orders.dependencies.services import (
    get_order_service,
    get_order_item_service,
    get_order_promotion_service,
    get_order_address_service,
    get_order_billing_service,
    get_order_receipt_service,
    get_order_pickup_service
)

from app.features.orders.services.order_service import OrderService
from app.features.orders.services.order_item_service import OrderItemService
from app.features.orders.services.order_promotion_service import (
    OrderPromotionService,
)
from app.features.orders.services.order_address_service import (
    OrderAddressService,
)
from app.features.orders.services.order_billing_service import (
    OrderBillingService,
)

from app.features.orders.use_cases.order_detail import (
    GetAdminOrderDetailUseCase,
)
from app.features.orders.services.order_receipt import OrderReceiptService

from app.features.locations.services.ubigeo_service import UbigeoService
from app.features.locations.dependencies.services import get_ubigeo_service, get_location_service
from app.features.orders.services.order_pickup_service import OrderPickupService
from app.features.locations.services.location_service import LocationService


def get_admin_order_detail_use_case(
    order_service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
    order_item_service: Annotated[
        OrderItemService,
        Depends(get_order_item_service),
    ],
    order_promotion_service: Annotated[
        OrderPromotionService,
        Depends(get_order_promotion_service),
    ],
    order_address_service: Annotated[
        OrderAddressService,
        Depends(get_order_address_service),
    ],
    order_billing_service: Annotated[
        OrderBillingService,
        Depends(get_order_billing_service),
    ],
    customer_service: Annotated[
        CustomerService,
        Depends(get_customer_service),
    ],
    ubigeo_service: Annotated[
        UbigeoService,
        Depends(get_ubigeo_service),
    ],
    order_receipt_service: Annotated[
        OrderReceiptService,
        Depends(get_order_receipt_service)
    ],
    order_pickup_service: OrderPickupService = Depends(
        get_order_pickup_service
    ),
    location_service: LocationService = Depends(
        get_location_service
    ),
) -> GetAdminOrderDetailUseCase:
    return GetAdminOrderDetailUseCase(
        order_service=order_service,
        order_item_service=order_item_service,
        order_promotion_service=order_promotion_service,
        order_address_service=order_address_service,
        order_billing_service=order_billing_service,
        customer_service=customer_service,
        ubigeo_service=ubigeo_service,
        order_receipt_service=order_receipt_service,
        order_pickup_service=order_pickup_service,
        location_service=location_service
    )