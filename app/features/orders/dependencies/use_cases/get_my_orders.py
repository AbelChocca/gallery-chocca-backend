from fastapi import Depends
from typing import Annotated

from app.features.customer.customer_service import (
    CustomerService,
)
from app.features.customer.dependencies.services.customer import (
    get_customer_service,
)


from app.features.orders.dependencies.services import (
    get_order_service,
    get_order_item_service,
)

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.services.order_item_service import (
    OrderItemService,
)
from app.features.orders.use_cases.get_my_orders import GetMyOrdersUseCase

def get_get_my_orders_use_case(
    customer_service: Annotated[
        CustomerService,
        Depends(get_customer_service),
    ],
    order_service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
    order_item_service: Annotated[
        OrderItemService,
        Depends(get_order_item_service),
    ],
) -> GetMyOrdersUseCase:
    return GetMyOrdersUseCase(
        customer_service=customer_service,
        order_service=order_service,
        order_item_service=order_item_service,
    )