from fastapi import Depends, Path, status
from typing import Annotated

from app.features.material.material_route import router
from app.features.material.dependency import get_activate_material_case
from app.features.material.use_cases.activate_material import ActivateMaterialUseCase
from app.core.authorization.dependencies import require_any_permission
from app.core.authorization.permissions import Permission

@router.patch(
    "/{material_id}/activate",
    status_code=status.HTTP_200_OK,
    summary="Activate material",
    dependencies=[
        require_any_permission(
            Permission.MATERIAL_CREATE,
            Permission.MATERIAL_DELETE,
            Permission.MATERIAL_UPDATE,
        )
    ]
)
async def activate_material(
    material_id: Annotated[int, Path(gt=0)],
    use_case: Annotated[
        ActivateMaterialUseCase,
        Depends(get_activate_material_case)
    ]
) -> None:

    await use_case.execute(material_id)