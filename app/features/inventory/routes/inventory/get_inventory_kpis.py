from fastapi import (
    Depends,
    status,
)
from typing import Annotated

from app.features.inventory.inventory_route import router
from app.features.inventory.schemas.inventory_schema import (
    InventoryKPIsRequest,
    InventoryKPIsResponse,
)
from app.features.inventory.use_cases.get_inventory_kpi import (
    GetInventoryKPIsUseCase,
)
from app.features.inventory.dependencies.inventory_cases import (
    get_inventory_kpis_use_case,
)
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


@router.get(
    "/kpis",
    response_model=InventoryKPIsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get inventory KPIs",
    dependencies=[
        require_permission(
            Permission.INVENTORY_READ,
        ),
    ],
)
async def get_inventory_kpis(
    request: Annotated[
        InventoryKPIsRequest,
        Depends(),
    ],
    use_case: Annotated[
        GetInventoryKPIsUseCase,
        Depends(get_inventory_kpis_use_case),
    ],
) -> InventoryKPIsResponse:

    result = await use_case.execute(
        owner_type=request.owner_type,
        current_location_id=request.current_location_id,
    )

    return InventoryKPIsResponse.model_validate(result)