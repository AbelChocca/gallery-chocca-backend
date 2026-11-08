
from typing import Annotated

from fastapi import Depends

from app.features.locations.location_router import router

from app.features.locations.services.location_service import (
    LocationService,
)
from app.features.locations.dependencies.services import (
    get_location_service,
)

from app.features.locations.schemas.location import (
    LocationResponse,
)


@router.get(
    "/pickup",
    response_model=list[LocationResponse],
    summary="List available pickup locations",
)
async def get_pickup_locations(
    service: Annotated[
        LocationService,
        Depends(get_location_service),
    ],
) -> list[LocationResponse]:

    locations = await service.get_pickup_locations()

    return [
        LocationResponse.model_validate(location)
        for location in locations
    ]
