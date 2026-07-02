from app.features.material.material_route import router
from app.features.material.mappers import MaterialResponseMapper
from app.features.material.schema import MaterialResponseSchema
from app.features.material.dependency import get_material_by_id_case
from app.features.material.use_cases.get_material_by_id import GetMaterialByIdUseCase
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, Path
from typing import Annotated


@router.get(
    "/{material_id}",
    status_code=status.HTTP_200_OK,
    summary="Get material detail",
    response_model=MaterialResponseSchema,
    dependencies=[
        require_permission(Permission.MATERIAL_READ)
    ]
)
async def get_supply(
    material_id: Annotated[
        int,
        Path(gt=0)
    ],
    use_case: Annotated[
        GetMaterialByIdUseCase,
        Depends(get_material_by_id_case)
    ]
) -> MaterialResponseSchema:
    material = await use_case.execute(material_id)

    return MaterialResponseMapper.to_schema(material)