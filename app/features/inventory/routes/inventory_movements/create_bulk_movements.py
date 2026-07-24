from typing import Annotated

from fastapi import Depends, status, Body

from app.features.inventory.inventory_route import router

from app.features.inventory.schemas.inventory_movement_schema import (
    CreateBulkMovementSchema
)

from app.features.inventory.dtos.inventory_movements import (
    CreateBulkMovementCommand,
    MovementItem
)

from app.features.inventory.use_cases.create_bulk_movement import (
    CreateBulkMovementUseCase
)
from app.core.authorization.dependencies import require_all_permissions
from app.core.authorization.permissions import Permission

from app.features.inventory.dependencies.inventory_movements_cases import (
    get_create_bulk_movement_use_case
)
from app.api.security.resolvers.sessions import get_user_id


@router.post(
    "/movements/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        require_all_permissions(
            Permission.INVENTORY_CREATE,
            Permission.INVENTORY_READ,
            Permission.INVENTORY_UPDATE
        )
    ]
)
async def create_bulk_movement(
    schema: Annotated[
        CreateBulkMovementSchema,
        Body()
    ],
    use_case: Annotated[
        CreateBulkMovementUseCase,
        Depends(
            get_create_bulk_movement_use_case
        )
    ],
    user_id: Annotated[int, Depends(get_user_id)],
) -> dict:
    command = CreateBulkMovementCommand(
        owner_type=schema.owner_type,
        type=schema.type,
        location_id=schema.location_id,
        reason=schema.reason,
        items=[
            MovementItem(
                owner_id=item.owner_id,
                owner_name=item.owner_name,
                owner_code=item.owner_code,
                quantity=item.quantity
            )
            for item in schema.items
        ],
    )

    return await use_case.execute(command, user_id)