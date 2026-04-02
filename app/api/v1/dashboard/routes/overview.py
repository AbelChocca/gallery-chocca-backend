from app.api.v1.dashboard.dashboard_route import router
from app.api.schemas.dashboard.schema import OverviewSchema
from app.api.schemas.user.user_schema import ReadUserSchema
from app.application.dashboard.cases.overview import OverviewCase
from app.api.security.resolvers.sessions import get_admin_session
from app.api.dependencies.dashboard.case_depends import get_overview_case

from fastapi import status, Depends
from typing import Annotated

@router.get(
    "/overview",
    response_model=OverviewSchema,
    status_code=status.HTTP_200_OK
)
async def overview(
    admin_payload: Annotated[dict, Depends(get_admin_session)],
    case: Annotated[OverviewCase, Depends(get_overview_case)]
) -> OverviewSchema:
    res = await case.execute()
    return OverviewSchema(
        admin=ReadUserSchema(**admin_payload),
        **res
    )