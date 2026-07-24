from fastapi import (
    Depends,
    status,
)

from typing import Annotated

from app.features.inventory.inventory_route import router

from app.features.inventory.schemas.inventory_product_schema import (
    ProductInventoryDetailSchema,
)

from app.features.inventory.use_cases.get_inventory_product_detail import (
    GetInventoryProductDetailUseCase,
)

from app.features.inventory.dependencies.inventory_cases import (
    get_inventory_product_detail_use_case,
)

from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


@router.get(
    "/products/{variant_size_id}",
    response_model=ProductInventoryDetailSchema,
    status_code=status.HTTP_200_OK,
    summary="Get inventory product detail",
    dependencies=[
        require_permission(Permission.INVENTORY_READ),
    ],
)
async def get_inventory_product_detail(
    variant_size_id: int,
    use_case: Annotated[
        GetInventoryProductDetailUseCase,
        Depends(get_inventory_product_detail_use_case),
    ],
) -> ProductInventoryDetailSchema:

    result = await use_case.execute(
        variant_size_id=variant_size_id,
    )

    return ProductInventoryDetailSchema.model_validate(
        result
    )