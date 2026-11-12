
from typing import Annotated

from fastapi import Depends, Query

from app.features.locations.location_router import router

from app.features.locations.services.location_service import (
    LocationService,
)
from app.features.locations.dependencies.services import (
    get_location_service,
)
from app.features.locations.schemas.location import (
    AdminLocationFiltersSchema,
    AdminLocationResponse,
)

from app.shared.pagination.schema import (
    PaginatedResponseSchema,
)


@router.get(
    "",
    summary="Get locations",
    response_model=PaginatedResponseSchema[AdminLocationResponse],
)
async def get_locations(
    service: Annotated[
        LocationService,
        Depends(get_location_service),
    ],
    filters: Annotated[
        AdminLocationFiltersSchema,
        Depends(),
    ],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PaginatedResponseSchema[AdminLocationResponse]:

    result = await service.get_locations(
        search=filters.search,
        location_type=filters.type,
        is_active=filters.is_active,
        pickup_enabled=filters.pickup_enabled,
        page=page,
        limit=limit,
    )

    return PaginatedResponseSchema[
        AdminLocationResponse
    ].model_validate(result)
