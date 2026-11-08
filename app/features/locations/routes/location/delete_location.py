
from typing import Annotated

from fastapi import Depends, Path, status

from app.features.locations.location_router import router

from app.features.locations.services.location_service import (
    LocationService,
)
from app.features.locations.dependencies.services import (
    get_location_service,
)

from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_permission(Permission.LOCATION_DELETE),
    ],
)
async def delete_location(
    location_id: Annotated[int, Path(gt=0)],
    service: Annotated[
        LocationService,
        Depends(get_location_service),
    ],
) -> None:

    await service.delete(
        location_id=location_id,
    )
