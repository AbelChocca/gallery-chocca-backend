from typing import Annotated

from fastapi import Depends

from app.features.locations.services.ubigeo_service import (
    UbigeoService,
)
from app.features.locations.services.location_service import (
    LocationService,
)

from app.infra.db.uow.dependency import (
    get_uow,
)
from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)


def get_ubigeo_service(
    uow: Annotated[
        UnitOfWork,
        Depends(get_uow),
    ],
) -> UbigeoService:
    return UbigeoService(
        ubigeo_repository=uow.ubigeos,
    )

def get_location_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> LocationService:

    return LocationService(
        repository=uow.locations,
    )
