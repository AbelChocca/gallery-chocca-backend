from app.features.inventory.inventory_route import router

from app.features.inventory.schemas.inventory_product_schema import (
    ProductInventoryRowSchema,
    InventoryProductFilterSchema,
)

from app.features.inventory.dependencies.inventory_cases import get_inventory_products_use_case

from app.features.inventory.use_cases.get_inventory_products import (
    GetInventoryProductsUseCase,
)

from app.shared.pagination.schema import PaginationSchema, PaginatedResponseSchema

from app.core.authorization.dependencies import (
    require_permission,
)

from app.core.authorization.permissions import Permission

from fastapi import (
    Depends,
    status,
)

from typing import Annotated


@router.get(
    "/products",
    response_model=PaginatedResponseSchema[ProductInventoryRowSchema],
    status_code=status.HTTP_200_OK,
    summary="Get inventory products",
    dependencies=[
        require_permission(Permission.INVENTORY_READ),
    ],
)
async def get_inventory_products(
    filter_schema: Annotated[
        InventoryProductFilterSchema,
        Depends(),
    ],
    pagination: Annotated[
        PaginationSchema,
        Depends(),
    ],
    use_case: Annotated[
        GetInventoryProductsUseCase,
        Depends(get_inventory_products_use_case),
    ],
) -> PaginatedResponseSchema[ProductInventoryRowSchema]:

    result = await use_case.execute(
        page=pagination.page,
        limit=pagination.limit,
        search=filter_schema.search,
        color=filter_schema.color,
        size=filter_schema.size,
        current_location_id=filter_schema.current_location_id,
    )

    return PaginatedResponseSchema.model_validate(result)