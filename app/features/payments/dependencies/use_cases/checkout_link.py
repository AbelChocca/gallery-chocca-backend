from typing import Annotated

from fastapi import Depends

from app.features.customer.customer_service import (
    CustomerService,
)
from app.features.customer.dependencies.services.customer import (
    get_customer_service,
)

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.dependencies.services import (
    get_order_service,
)

from app.features.payments.services.payment_service import (
    PaymentService,
)
from app.features.payments.dependencies.services import (
    get_payment_service,
)

from app.features.payments.use_cases.checkout_link import (
    CreatePaymentCheckoutUseCase,
)


def get_create_payment_checkout_use_case(
    order_service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
    customer_service: Annotated[
        CustomerService,
        Depends(get_customer_service),
    ],
    payment_service: Annotated[
        PaymentService,
        Depends(get_payment_service),
    ],
) -> CreatePaymentCheckoutUseCase:
    return CreatePaymentCheckoutUseCase(
        order_service=order_service,
        customer_service=customer_service,
        payment_service=payment_service,
    )