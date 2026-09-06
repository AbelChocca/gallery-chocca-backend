from fastapi import (
    Depends,
    status,
)
from typing import Annotated

from app.features.inventory.inventory_route import router
from app.features.inventory.schemas.inventory_schema import (
    InventoryConsumptionChartRequest,
    InventoryConsumptionChartResponse,
)
from app.features.inventory.use_cases.get_inventory_consumption_chart import (
    GetInventoryConsumptionChartUseCase,
)
from app.features.inventory.dependencies.inventory_cases import (
    get_inventory_consumption_chart_use_case,
)
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


@router.get(
    "/consumption",
    response_model=InventoryConsumptionChartResponse,
    status_code=status.HTTP_200_OK,
    summary="Get inventory consumption chart",
    dependencies=[
        require_permission(
            Permission.INVENTORY_READ,
        ),
    ],
)
async def get_inventory_consumption_chart(
    request: Annotated[
        InventoryConsumptionChartRequest,
        Depends(),
    ],
    use_case: Annotated[
        GetInventoryConsumptionChartUseCase,
        Depends(get_inventory_consumption_chart_use_case),
    ],
) -> InventoryConsumptionChartResponse:
    result = await use_case.execute(
        owner_type=request.owner_type,
        owner_id=request.owner_id,
        current_location_id=request.current_location_id,
        days=request.days,
    )

    return InventoryConsumptionChartResponse.model_validate(result)