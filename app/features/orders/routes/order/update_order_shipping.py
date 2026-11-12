from typing import Annotated

from fastapi import Depends, status

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import (
    Permission,
)

from app.features.orders.services.order_service import OrderService
from app.features.orders.dependencies.services import get_order_service

from app.features.orders.schemas.order import (
    UpdateOrderShippingRequestSchema,
    UpdateOrderShippingResponseSchema,
)

from app.features.orders.order_router import router


@router.patch(
    "/{order_id}/shipping",
    response_model=UpdateOrderShippingResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update order shipping",
    dependencies=[
        require_all_permissions(
            Permission.ORDER_UPDATE,
        ),
    ],
)
async def update_order_shipping(
    order_id: int,
    payload: UpdateOrderShippingRequestSchema,
    order_service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
):
    result = await order_service.update_shipping(
        order_id=order_id,
        shipping_cost=payload.shipping_cost,
    )

    return UpdateOrderShippingResponseSchema.model_validate(result)