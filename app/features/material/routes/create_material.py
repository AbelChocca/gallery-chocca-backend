from app.features.material.material_route import router
from app.features.material.schema import CreateSupplyRequest
from app.features.material.dto.material import CreateMaterialDTO
from app.features.material.dto.material_component import CreateMaterialComponentDTO
from app.features.inventory.dtos.inventory import CreateInventoryCommand
from app.features.material.dependency import get_create_material_case
from app.features.material.use_cases.create_material import CreateMaterialUseCase
from app.api.helpers.validators import validate_image
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission
from app.api.security.resolvers.sessions import get_user_id

from fastapi import (
    Depends,
    UploadFile,
    File,
    status
)
from typing import Annotated

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create material",
    dependencies=[
        require_permission(Permission.MATERIAL_CREATE)
    ]
)
async def create_supply(
    request: Annotated[
        CreateSupplyRequest,
        Depends(CreateSupplyRequest.as_form)
    ],
    user_id: Annotated[int, Depends(get_user_id)],
    case: Annotated[
        CreateMaterialUseCase,
        Depends(get_create_material_case)
    ],
    image_file: UploadFile | None = File(None)
) -> None:
    image_file = await validate_image(image_file)

    data = request.model_dump()

    data["components"] = [
        CreateMaterialComponentDTO(**component)
        for component in data["components"]
    ]

    data["inventories"] = [
        CreateInventoryCommand(**inventory)
        for inventory in data["inventories"]
    ]

    await case.execute(
        command=CreateMaterialDTO(**data),
        user_id=user_id,
        image_file=image_file.file if image_file else None
    )