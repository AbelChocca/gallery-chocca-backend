from app.features.inventory.inventory_route import router

from app.features.inventory.schemas.inventory_material_schema import (
    MaterialInventoryRowSchema,
    InventoryMaterialFilterSchema,
)

from app.features.inventory.dependencies.inventory_cases import (
    get_inventory_materials_use_case,
)

from app.features.inventory.use_cases.get_inventory_materials import (
    GetInventoryMaterialsUseCase,
)

from app.shared.pagination.schema import (
    PaginationSchema,
    PaginatedResponseSchema,
)

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
    "/materials",
    response_model=PaginatedResponseSchema[MaterialInventoryRowSchema],
    status_code=status.HTTP_200_OK,
    summary="Get inventory materials",
    dependencies=[
        require_permission(Permission.INVENTORY_READ),
    ],
)
async def get_inventory_materials(
    filter_schema: Annotated[
        InventoryMaterialFilterSchema,
        Depends(),
    ],
    pagination: Annotated[
        PaginationSchema,
        Depends(),
    ],
    use_case: Annotated[
        GetInventoryMaterialsUseCase,
        Depends(get_inventory_materials_use_case),
    ],
) -> PaginatedResponseSchema[MaterialInventoryRowSchema]:

    result = await use_case.execute(
        page=pagination.page,
        limit=pagination.limit,

        search=filter_schema.search,

        material_type=filter_schema.material_type,
        availability_status=filter_schema.availability_status,
        is_active=filter_schema.is_active,

        current_location_id=filter_schema.current_location_id,
    )

    return PaginatedResponseSchema.model_validate(result)