from typing import Annotated

from fastapi import Depends

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

from app.features.orders.dependencies.use_cases.get_my_orders import (
    get_get_my_orders_use_case,
)

from app.features.orders.use_cases.get_my_orders import (
    GetMyOrdersUseCase,
)

from app.features.orders.schemas.order import (
    GetMyOrderResponseSchema,
)
from app.features.orders.order_router import router
from app.api.security.rate_limiter.ratelimiter import limiter


@router.get(
    "/me",
    response_model=list[GetMyOrderResponseSchema],
    dependencies=[Depends(limiter.limiter(60, 60))],
    summary="Get current customer's orders",
)
async def get_my_orders(
    use_case: Annotated[
        GetMyOrdersUseCase,
        Depends(get_get_my_orders_use_case),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
) -> list[GetMyOrderResponseSchema]:

    orders = await use_case.execute(
        user_id=owner.user_id,
        session_id=owner.session_id,
    )

    return [
        GetMyOrderResponseSchema.model_validate(order)
        for order in orders
    ]