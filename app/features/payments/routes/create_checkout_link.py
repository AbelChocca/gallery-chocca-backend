from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import (
    Permission,
)

from app.features.payments.dependencies.use_cases.checkout_link import (
    get_create_payment_checkout_use_case,
)

from app.features.payments.schemas.payment_schema import (
    CreatePaymentCheckoutRequestSchema,
    CreatePaymentCheckoutResponseSchema,
)

from app.features.payments.types.payment import (
    CreatePaymentCheckoutInput,
)

from app.features.payments.use_cases.checkout_link import (
    CreatePaymentCheckoutUseCase,
)

from app.features.payments.payment_route import router

@router.post(
    "/{order_id}/payment-link",
    response_model=CreatePaymentCheckoutResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Create order payment link",
    dependencies=[
        require_all_permissions(
            Permission.ORDER_PAYMENT_CREATE,
        ),
    ],
)
async def create_order_payment_link(
    order_id: int,
    payload: CreatePaymentCheckoutRequestSchema,
    use_case: Annotated[
        CreatePaymentCheckoutUseCase,
        Depends(
            get_create_payment_checkout_use_case
        ),
    ],
):
    result = await use_case.execute(
        order_id=order_id,
        input=CreatePaymentCheckoutInput(
            send_email=payload.send_email,
            expiration_date=payload.expiration_date,
        ),
    )   

    return CreatePaymentCheckoutResponseSchema.model_validate(result)