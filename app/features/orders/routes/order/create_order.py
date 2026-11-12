# app/features/orders/routes/create_order.py

from typing import Annotated

from fastapi import Depends, status

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)
from app.features.orders.order_router import router
from app.features.orders.dependencies.use_cases.create_order import (
    get_create_order_use_case,
)
from app.features.orders.schemas.order import (
    CreateOrderRequestSchema,
    CreateOrderResponseSchema,
)
from app.features.orders.types.order import (
    CreateOrderInput,
    CreateOrderCustomerDTO,
    CreateOrderAddressDTO,
    CreateOrderBillingDTO,
    CreateOrderPickupDTO
)
from app.api.security.rate_limiter.ratelimiter import limiter
from app.features.orders.use_cases.create_order import (
    CreateOrderUseCase,
)


@router.post(
    "",
    response_model=CreateOrderResponseSchema,
    dependencies=[Depends(limiter.limiter(5, 60))],
    status_code=status.HTTP_201_CREATED,
    summary="Create order",
)
async def create_order(
    payload: CreateOrderRequestSchema,
    use_case: Annotated[
        CreateOrderUseCase,
        Depends(get_create_order_use_case),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
) -> CreateOrderResponseSchema:

    result = await use_case.execute(
        CreateOrderInput(
            user_id=owner.user_id,
            session_id=owner.session_id,

            customer=(
                CreateOrderCustomerDTO(
                    **payload.customer.model_dump()
                )
                if payload.customer
                else None
            ),

            delivery_method=payload.delivery_method,
            address=(
                CreateOrderAddressDTO(**payload.address.model_dump())
                if payload.address is not None
                else None
            ),
            pickup=(
                CreateOrderPickupDTO(**payload.pickup.model_dump())
                if payload.pickup is not None
                else None
            ),

            billing=(
                CreateOrderBillingDTO(
                    **payload.billing.model_dump()
                )
                if payload.billing
                else None
            ),

            coupon_code=payload.coupon_code,
            payment_method=payload.payment_method,
        )
    )

    return CreateOrderResponseSchema.model_validate(
        result
    )