from typing import Annotated

from fastapi import Depends, status

from app.api.security.resolvers.sessions import get_user_info
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission
from app.features.dashboard.dashboard_route import router
from app.features.dashboard.dependency import (
    get_dashboard_overview_use_case,
)
from app.features.dashboard.schema import OverviewSchema
from app.features.dashboard.use_cases.get_dashboard_overview import (
    GetDashboardOverviewUseCase,
)
from app.features.user.user_schema import ReadUserSchema


@router.get(
    "/overview",
    response_model=OverviewSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_permission(Permission.DASHBOARD_READ),
    ],
)
async def overview(
    use_case: Annotated[
        GetDashboardOverviewUseCase,
        Depends(get_dashboard_overview_use_case),
    ],
    user_info: ReadUserSchema = Depends(get_user_info),
) -> OverviewSchema:
    res = await use_case.execute()

    return OverviewSchema(
        admin=user_info,
        **res.dto_to_dict(),
    )