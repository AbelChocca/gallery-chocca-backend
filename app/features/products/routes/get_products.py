from typing import Annotated

from fastapi import Depends, status

from app.features.products.product_route import router
from app.features.products.schema import (
    FilterSchema,
    GetGridProductsResponse,
)
from app.features.products.mappers.schema_mapper import (
    InputSchemaMapper,
)
from app.features.products.parsers import filter_dep
from app.features.products.dependency import (
    get_products_use_case,
)
from app.features.products.use_cases.get_products import (
    GetProductsUseCase,
)

from app.features.customer.dtos.customer import (
    CustomerPricingContext,
)
from app.features.customer.helpers.get_customer_pricing_context import (
    get_customer_pricing_context,
)

from app.shared.pagination.schema import (
    PaginationSchema,
)


@router.get(
    "/all",
    response_model=GetGridProductsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all products",
)
async def get_products(
    filter_schema: Annotated[
        FilterSchema,
        Depends(filter_dep),
    ],
    use_case: Annotated[
        GetProductsUseCase,
        Depends(get_products_use_case),
    ],
    pagination: Annotated[
        PaginationSchema,
        Depends(),
    ],
    customer: Annotated[
        CustomerPricingContext | None,
        Depends(get_customer_pricing_context),
    ],
) -> GetGridProductsResponse:

    filter_command = (
        InputSchemaMapper.to_filter_command(
            filter_schema
        )
    )

    res = await use_case.execute(
        command=filter_command,
        customer_id=(
            customer.customer_id
            if customer
            else None
        ),
        customer_type=(
            customer.customer_type
            if customer
            else None
        ),
        page=pagination.page,
        limit=pagination.limit,
    )

    return GetGridProductsResponse.model_validate(
        res
    )