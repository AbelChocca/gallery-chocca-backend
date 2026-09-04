from fastapi import Depends

from app.features.balancing.routes.other_current_liability.other_current_liability_router import other_current_liability_router
from app.features.balancing.services.other_current_liability_service import OtherCurrentLiabilityService
from app.features.balancing.dependencies.other_current_liability.service import get_other_current_liability_service
from app.features.balancing.schemas.other_current_liablility_schema import OtherCurrentLiabilityFilterSchema, OtherCurrentLiabilityResponseSchema


@other_current_liability_router.get(
    "",
    response_model=list[
        OtherCurrentLiabilityResponseSchema
    ],
)
async def get_other_current_liabilities(
    filters: OtherCurrentLiabilityFilterSchema = Depends(),
    service: OtherCurrentLiabilityService = Depends(
        get_other_current_liability_service
    ),
):
    result = await service.find(
        balance_snapshot_id=filters.balance_snapshot_id,
        category=filters.category,
        status=filters.status,
    )

    return result