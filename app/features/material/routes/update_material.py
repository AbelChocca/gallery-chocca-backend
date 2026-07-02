from app.features.material.material_route import router
from app.features.material.schema import UpdateMaterialRequest
from app.features.material.dto import UpdateMaterialDTO
from app.features.material.service import MaterialService
from app.features.material.dependency import get_material_service

from app.core.authorization.dependencies import require_any_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, Path
from typing import Annotated

@router.patch(
    "/{material}",
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
    request: UpdateMaterialRequest,
    service: Annotated[
        MaterialService,
        Depends(get_material_service)
    ]
):
    await service.update(
        supply_id=material_id,
        dto=UpdateMaterialDTO(
            **request.model_dump()
        )
    )

    return None