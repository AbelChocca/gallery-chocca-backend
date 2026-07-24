from fastapi import (
    Depends,
    status,
)

from typing import Annotated

from app.features.inventory.inventory_route import router

from app.features.inventory.schemas.inventory_material_schema import (
    MaterialInventoryDetailSchema,
)

from app.features.inventory.use_cases.get_inventory_material_detail import (
    GetInventoryMaterialDetailUseCase,
)

from app.features.inventory.dependencies.inventory_cases import (
    get_inventory_material_detail_use_case,
)

from app.core.authorization.dependencies import (
    require_permission,
)

from app.core.authorization.permissions import (
    Permission,
)


@router.get(
    "/materials/{material_id}",
    response_model=MaterialInventoryDetailSchema,
    status_code=status.HTTP_200_OK,
    summary="Get inventory material detail",
    dependencies=[
        require_permission(
            Permission.INVENTORY_READ,
        ),
    ],
)
async def get_inventory_material_detail(
    material_id: int,
    use_case: Annotated[
        GetInventoryMaterialDetailUseCase,
        Depends(
            get_inventory_material_detail_use_case,
        ),
    ],
) -> MaterialInventoryDetailSchema:

    result = await use_case.execute(
        material_id=material_id,
    )

    return MaterialInventoryDetailSchema.model_validate(
        result
    )