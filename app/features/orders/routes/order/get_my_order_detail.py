# app/features/orders/routes/get_my_order_detail.py

from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

from app.features.orders.dependencies.use_cases.get_my_order_detail import (
    get_my_order_detail_use_case,
)

from app.features.orders.use_cases.get_my_order_detail import (
    GetMyOrderDetailUseCase,
)

from app.features.orders.schemas.order import (
    MyOrderDetailResponseSchema,
)

from app.features.orders.order_router import (
    router,
)


@router.get(
    "/me/{order_id}",
    response_model=(
        MyOrderDetailResponseSchema
    ),
    status_code=(
        status.HTTP_200_OK
    ),
    summary="Get current customer's order detail",
)
async def get_my_order_detail(
    order_id: int,

    use_case: Annotated[
        GetMyOrderDetailUseCase,
        Depends(
            get_my_order_detail_use_case
        ),
    ],

    owner: Annotated[
        OwnerSession,
        Depends(
            get_session_owner
        ),
    ],
) -> MyOrderDetailResponseSchema:

    result = await (
        use_case.execute(
            order_id=order_id,
            user_id=owner.user_id,
            session_id=owner.session_id,
        )
    )

    return (
        MyOrderDetailResponseSchema
        .model_validate(
            result
        )
    )