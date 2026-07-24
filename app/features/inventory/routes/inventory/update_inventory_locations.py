from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.core.authorization.dependencies import (
    require_permission,
)
from app.core.authorization.permissions import Permission

from app.features.inventory.inventory_route import router

from app.features.inventory.dependencies.inventory_cases import (
    get_update_inventory_locations_use_case,
)

from app.features.inventory.schemas.inventory_schema import (
    UpdateInventoryLocationSchema,
)

from app.features.inventory.use_cases.update_inventory_locations import (
    UpdateInventoryLocationsUseCase,
)
from app.features.inventory.dtos.inventory import (
    UpdateInventoryLocationDTO,
)
from app.features.inventory.types.inventory_movement import InventoryOwnerType


@router.put(
    "/{owner_type}/{owner_id}/locations",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update inventory locations",
    dependencies=[
        require_permission(
            Permission.INVENTORY_UPDATE,
        ),
    ],
)
async def update_inventory_locations(
    owner_type: InventoryOwnerType,
    owner_id: int,
    locations: list[UpdateInventoryLocationSchema],
    use_case: Annotated[
        UpdateInventoryLocationsUseCase,
        Depends(
            get_update_inventory_locations_use_case,
        ),
    ],
) -> None:

    await use_case.execute(
        owner_id=owner_id,
        owner_type=owner_type,
        locations=[
            UpdateInventoryLocationDTO(
                **location.model_dump()
            )
            for location in locations
        ],
    )