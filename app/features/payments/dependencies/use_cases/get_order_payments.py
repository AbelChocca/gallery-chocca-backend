from typing import Annotated

from fastapi import Depends

from app.features.payments.dependencies.services import (
    get_payment_event_service,
    get_payment_service
)

from app.features.payments.services.payment_service import (
    PaymentService,
)
from app.features.payments.services.payment_event_service import (
    PaymentEventService,
)

from app.features.payments.use_cases.get_order_payments import (
    GetOrderPaymentsUseCase,
)


def get_order_payments_use_case(
    payment_service: Annotated[
        PaymentService,
        Depends(get_payment_service),
    ],
    payment_event_service: Annotated[
        PaymentEventService,
        Depends(get_payment_event_service),
    ],
) -> GetOrderPaymentsUseCase:

    return GetOrderPaymentsUseCase(
        payment_service=payment_service,
        payment_event_service=(
            payment_event_service
        ),
    )