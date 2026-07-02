from fastapi import Depends, Path, status
from typing import Annotated

from app.features.material.material_route import router
from app.features.material.dependency import get_deactivate_material_case
from app.features.material.use_cases.deactivate_material import DeactivateMaterialUseCase
from app.core.authorization.dependencies import require_any_permission
from app.core.authorization.permissions import Permission

@router.delete(
    "/{material_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deactivate material",
    dependencies=[
        require_any_permission(
            Permission.MATERIAL_CREATE,
            Permission.MATERIAL_DELETE,
            Permission.MATERIAL_UPDATE
        )
    ]
)
async def deactivate_material(
    material_id: Annotated[int, Path(gt=0)],
    use_case: Annotated[
        DeactivateMaterialUseCase,
        Depends(get_deactivate_material_case)
    ]
) -> None:

    await use_case.execute(material_id)