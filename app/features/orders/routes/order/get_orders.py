from typing import Annotated

from fastapi import Depends, Query, status

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import (
    Permission,
)

from app.features.orders.types.order import OrderFilters
from app.features.orders.services.order_service import OrderService
from app.features.orders.schemas.order import (
    AdminOrderFiltersSchema,
    AdminOrderListItemResponseSchema,
)

from app.shared.pagination.schema import (
    PaginationSchema,
    PaginatedResponseSchema,
)

from app.shared.datetime import (
    to_datetime_range,
)
from app.features.orders.dependencies.services import get_order_service
from app.features.orders.order_router import router


@router.get(
    "",
    response_model=PaginatedResponseSchema[
        AdminOrderListItemResponseSchema
    ],
    summary="Get admin orders",
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_all_permissions(
            Permission.ORDER_READ,
        ),
    ],
)
async def get_admin_orders(
    filters: Annotated[
        AdminOrderFiltersSchema,
        Query(),
    ],
    pagination: Annotated[
        PaginationSchema,
        Depends(),
    ],
    order_service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
):
    date_range = to_datetime_range(
        start=filters.created_at_from,
        end=filters.created_at_to,
    )

    result = await order_service.get_admin_orders(
        filters=OrderFilters(
            search=filters.search,
            status=filters.status,
            created_at_from=date_range.start,
            created_at_to=date_range.end,
        ),
        page=pagination.page,
        limit=pagination.limit,
    )

    return result