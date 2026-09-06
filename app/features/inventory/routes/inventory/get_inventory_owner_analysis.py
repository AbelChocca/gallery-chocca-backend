from fastapi import (
    Depends,
    status,
)
from typing import Annotated

from app.features.inventory.inventory_route import router
from app.features.inventory.schemas.inventory_schema import (
    InventoryAnalysisResponse,
    InventoryAnalysisRequest
)
from app.features.inventory.use_cases.get_inventory_analysis import (
    GetInventoryAnalysisUseCase,
)
from app.features.inventory.dependencies.inventory_cases import (
    get_inventory_analysis_use_case,
)
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


@router.get(
    "/analysis",
    response_model=InventoryAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get inventory analysis",
    dependencies=[
        require_permission(
            Permission.INVENTORY_READ,
        ),
    ],
)
async def get_inventory_analysis(
    request: Annotated[
        InventoryAnalysisRequest,
        Depends(),
    ],
    use_case: Annotated[
        GetInventoryAnalysisUseCase,
        Depends(get_inventory_analysis_use_case),
    ],
) -> InventoryAnalysisResponse:

    result = await use_case.execute(
        owner_type=request.owner_type,
        owner_id=request.owner_id,
    )

    return InventoryAnalysisResponse.model_validate(result)