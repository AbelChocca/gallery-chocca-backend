from fastapi import (
    Depends,
    Query,
)

from app.features.customer.dependencies.services.customer import (
    get_customer_service,
)
from app.features.customer.schemas.customer import (
    CustomerSearchOptionResponseSchema,
)
from app.features.customer.customer_service import (
    CustomerService,
)

from app.shared.pagination.schema import (
    PaginatedResponseSchema,
)

from app.features.customer.customer_route import router


@router.get(
    "/search-options",
    response_model=PaginatedResponseSchema[
        CustomerSearchOptionResponseSchema
    ],
)
async def search_customer_options(
    search: str | None = Query(
        default=None,
        max_length=150,
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    customer_service: CustomerService = Depends(
        get_customer_service
    ),
) -> PaginatedResponseSchema[
    CustomerSearchOptionResponseSchema
]:
    result = (
        await customer_service.search_options(
            search=search,
            page=page,
            limit=limit,
        )
    )

    return PaginatedResponseSchema[
        CustomerSearchOptionResponseSchema
    ].model_validate(result)