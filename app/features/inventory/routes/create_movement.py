from app.features.inventory.inventory_route import router
from app.features.inventory.inventory_schema import CreateMovementSchema
from app.features.inventory.use_cases.create_movement import CreateMovementUseCase
from app.features.inventory.dependency import (
    get_create_movement_use_case
)
from app.features.inventory.dto import CreateMovementCommand
from app.core.authorization.dependencies import require_all_permissions
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
    use_case: Annotated[
        CreateMovementUseCase,
        Depends(get_create_movement_use_case)
    ]
) -> dict:
    command = CreateMovementCommand(
        owner_id=schema.owner_id,
        owner_type=schema.owner_type,
        type=schema.type,
        quantity=schema.quantity,
        reason=schema.reason
    )
    return await use_case.execute(command)