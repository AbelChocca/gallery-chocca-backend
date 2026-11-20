from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.features.inventory.inventory_route import router

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import Permission

from app.features.inventory.schemas.inventory_location_schema import (
    InventoryLocationFiltersSchema,
    InventoryLocationResponseSchema,
)

from app.features.inventory.use_cases.get_inventory_locations import (
    GetInventoryLocationsUseCase,
)
from app.features.inventory.dependencies.inventory_cases import (
    get_inventory_locations_use_case,
)


@router.get(
    "/locations",
    response_model=list[InventoryLocationResponseSchema],
    dependencies=[
        require_all_permissions(
            Permission.INVENTORY_LOCATION_READ,
        )
    ],
)
async def get_inventory_locations(
    filters: Annotated[
        InventoryLocationFiltersSchema,
        Depends(),
    ],
    use_case: Annotated[
        GetInventoryLocationsUseCase,
        Depends(get_inventory_locations_use_case),
    ],
) -> list[InventoryLocationResponseSchema]:

    if (filters.owner_type is None) != (filters.owner_id is None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "owner_type y owner_id deben "
                "enviarse juntos."
            ),
        )

    locations = await use_case.execute(
        search=filters.search,
        is_active=filters.is_active,
        owner_type=filters.owner_type,
        owner_id=filters.owner_id,
    )

    return [
        InventoryLocationResponseSchema.model_validate(location)
        for location in locations
    ]