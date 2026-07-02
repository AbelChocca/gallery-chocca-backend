from app.features.material.material_route import router
from app.features.material.schema import CreateSupplyRequest
from app.features.material.dto import CreateMaterialDTO
from app.features.material.dependency import get_create_material_case
from app.features.material.use_cases.create_material import CreateMaterialUseCase
from app.api.helpers.validators import validate_image
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import (
    Depends,
    UploadFile,
    File,
    status
)
from typing import Annotated

@router.post(
    "/",
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
    case: Annotated[
        CreateMaterialUseCase,
        Depends(get_create_material_case)
    ],
    image_file: UploadFile | None = File(None)
) -> None:
    image_file = await validate_image(image_file)

    await case.execute(
        command=CreateMaterialDTO(
            **request.model_dump()
        ),
        image_file=image_file.file if image_file else None
    )