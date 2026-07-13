from app.features.material.material_route import router
from app.features.material.schema import UpdateMaterialRequest
from app.features.material.dto.material import UpdateMaterialDTO
from app.features.material.dto.material_component import CreateMaterialComponentDTO
from app.api.helpers.validators import validate_image

from app.core.authorization.dependencies import require_any_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, Path, UploadFile, File
from typing import Annotated

from app.features.material.dependency import get_update_material_use_case
from app.features.material.use_cases.update_material import UpdateMaterialUseCase

@router.patch(
    "/{material_id}",
    status_code=status.HTTP_200_OK,
    summary="Update supply",
    dependencies=[
        require_any_permission(
            Permission.MATERIAL_UPDATE,
            Permission.MATERIAL_CREATE,
            Permission.MATERIAL_DELETE
        )
    ]
)
async def update_supply(
    material_id: Annotated[
        int,
        Path(gt=0)
    ],
    request: Annotated[
        UpdateMaterialRequest,
        Depends(UpdateMaterialRequest.as_form)
    ],
    use_case: Annotated[
        UpdateMaterialUseCase,
        Depends(get_update_material_use_case)
    ],
    image_file: UploadFile | None = File(None),
):
    image_file = await validate_image(image_file)

    data = request.model_dump(exclude_unset=True, exclude={"components"})

    if request.components is not None:
        data["components"] = [
            CreateMaterialComponentDTO(
                fiber_type=component.fiber_type,
                percentage=component.percentage,
            )
            for component in request.components
        ]

    await use_case.execute(
        material_id=material_id,
        command=UpdateMaterialDTO(**data),
        image_file=image_file.file if image_file else None,
    )

    return None