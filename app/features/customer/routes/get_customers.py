from typing import Annotated

from fastapi import Depends, status

from app.features.customer.customer_route import router
from app.features.customer.customer_service import (
    CustomerService,
)
from app.features.customer.dependencies.services.customer import (
    get_customer_service,
)
from app.features.customer.dtos.customer import (
    CustomerFilters,
)
from app.features.customer.schemas.customer import (
    CustomerResponseSchema,
)
from app.shared.pagination.schema import (
    PaginationSchema,
    PaginatedResponseSchema
)


@router.get(
    "",
    response_model=PaginatedResponseSchema[CustomerResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get customers",
)
async def get_customers(
    filters: Annotated[
        CustomerFilters,
        Depends(),
    ],
    pagination: Annotated[
        PaginationSchema,
        Depends(),
    ],
    service: Annotated[
        CustomerService,
        Depends(get_customer_service),
    ],
) -> PaginatedResponseSchema[CustomerResponseSchema]:

    result = await service.get_customers(
        filters=filters,
        page=pagination.page,
        limit=pagination.limit,
    )

    return PaginatedResponseSchema[CustomerResponseSchema].model_validate(
        result
    )