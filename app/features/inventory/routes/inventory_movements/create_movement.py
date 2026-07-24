from app.features.inventory.inventory_route import router
from app.features.inventory.schemas.inventory_movement_schema import CreateMovementSchema
from app.features.inventory.use_cases.create_movement import CreateMovementUseCase
from app.features.inventory.dependencies.inventory_movements_cases import (
    get_create_movement_use_case
)
from app.features.inventory.dtos.inventory_movements import CreateMovementCommand
from app.core.authorization.dependencies import require_all_permissions
from app.api.security.resolvers.sessions import get_user_id
from app.core.authorization.permissions import Permission


from fastapi import Depends, status, Body
from typing import Annotated

@router.post(
    '/movements',
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        require_all_permissions(
            Permission.INVENTORY_CREATE,
            Permission.INVENTORY_READ,
            Permission.INVENTORY_UPDATE
        )
    ]
)
async def create_movement(
    schema: Annotated[CreateMovementSchema, Body()],
    user_id: Annotated[int, Depends(get_user_id)],
    use_case: Annotated[
        CreateMovementUseCase,
        Depends(get_create_movement_use_case)
    ]
) -> dict:
    command = CreateMovementCommand(
        owner_id=schema.owner_id,
        owner_type=schema.owner_type,
        owner_code=schema.owner_code,
        owner_name=schema.owner_name,
        type=schema.type,
        quantity=schema.quantity,
        location_id=schema.location_id,
        performed_by=user_id,
        reason=schema.reason
    )
    return await use_case.execute(command)