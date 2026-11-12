from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.features.payments.payment_route import (
    router,
)

from app.features.payments.dependencies.use_cases.get_order_payments import (
    get_order_payments_use_case,
)

from app.features.payments.schemas.payment_schema import (
    PaymentDetailResponseSchema,
)

from app.features.payments.use_cases.get_order_payments import (
    GetOrderPaymentsUseCase,
)


@router.get(
    "/{order_id}",
    response_model=list[
        PaymentDetailResponseSchema
    ],
    status_code=status.HTTP_200_OK,
    summary="Get order payments with events",
)
async def get_order_payments(
    order_id: int,
    use_case: Annotated[
        GetOrderPaymentsUseCase,
        Depends(
            get_order_payments_use_case
        ),
    ],
) -> list[
    PaymentDetailResponseSchema
]:

    result = await use_case.execute(
        order_id=order_id,
    )

    return [
        PaymentDetailResponseSchema
        .model_validate(payment)
        for payment in result
    ]