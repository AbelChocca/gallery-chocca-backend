from app.features.dashboard.dashboard_route import router
from app.features.dashboard.schema import OverviewSchema
from app.features.user.user_schema import ReadUserSchema
from app.api.security.resolvers.sessions import get_admin_session
from app.features.dashboard.service import DashboardService
from app.features.dashboard.dependency import get_dashboard_service

from fastapi import status, Depends
from typing import Annotated

@router.get(
    "/overview",
    response_model=OverviewSchema,
    status_code=status.HTTP_200_OK
)
async def overview(
    admin_payload: Annotated[dict, Depends(get_admin_session)],
    service: Annotated[DashboardService, Depends(get_dashboard_service)]
) -> OverviewSchema:
    res = await service.overview()
    return OverviewSchema(
        admin=ReadUserSchema(**admin_payload),
        **res
    )