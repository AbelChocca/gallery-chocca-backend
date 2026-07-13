from app.features.material.material_route import router
from app.features.material.schema import GetMaterialsQuerySchema, MaterialPaginatedResponseSchema
from app.features.material.dto.material import MaterialFilters
from app.features.material.mappers import MaterialPaginatedResponseMapper
from app.features.material.use_cases.get_materials import GetMaterialsUseCase
from app.features.material.dependency import get_materials_case

from app.shared.pagination.schema import PaginationSchema
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends
from typing import Annotated

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get materials",
    response_model=MaterialPaginatedResponseSchema,
    dependencies=[
        require_permission(Permission.MATERIAL_READ)
    ]
)
async def get_supplies(
    query: Annotated[
        GetMaterialsQuerySchema,
        Depends()
    ],
    pagination: Annotated[PaginationSchema, Depends()],
    use_case: Annotated[
        GetMaterialsUseCase,
        Depends(get_materials_case)
    ],
) -> MaterialPaginatedResponseSchema:
    response = await use_case.execute(
        filters=MaterialFilters(
            search=query.search,
            company=query.company,
            material_type=query.material_type,
            is_active=query.is_active,
            availability_status=query.availability_status
        ),
        page=pagination.page,
        limit=pagination.limit
    )

    return MaterialPaginatedResponseMapper.to_schema(
        entities=response.items,
        total_items=response.total_items,
        total_pages=response.pagination.total_pages,
        current_page=response.pagination.current_page
    )
