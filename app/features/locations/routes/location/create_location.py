
from typing import Annotated

from fastapi import Depends, status

from app.features.locations.location_router import router

from app.features.locations.schemas.location import (
    CreateLocationRequestSchema,
)
from app.features.locations.services.location_service import (
    LocationService,
)
from app.features.locations.dependencies.services import (
    get_location_service,
)

from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


@router.post(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_permission(Permission.LOCATION_CREATE),
    ],
)
async def create_location(
    payload: CreateLocationRequestSchema,
    service: Annotated[
        LocationService,
        Depends(get_location_service),
    ],
) -> None:

    await service.create(
        **payload.model_dump(),
    )
