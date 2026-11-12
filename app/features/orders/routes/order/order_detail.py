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

from app.features.orders.dependencies.use_cases.order_detail import (
    get_admin_order_detail_use_case,
)

from app.features.orders.schemas.order import (
    AdminOrderDetailResponseSchema,
)

from app.features.orders.use_cases.order_detail import (
    GetAdminOrderDetailUseCase,
)

from app.features.orders.order_router import router


@router.get(
    "/{order_id}",
    response_model=AdminOrderDetailResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get admin order detail",
    dependencies=[
        require_all_permissions(
            Permission.ORDER_READ,
        ),
    ],
)
async def get_admin_order_detail(
    order_id: int,
    use_case: Annotated[
        GetAdminOrderDetailUseCase,
        Depends(
            get_admin_order_detail_use_case
        ),
    ],
):
    result = await use_case.execute(
        order_id=order_id,
    )


    return AdminOrderDetailResponseSchema.model_validate(result)