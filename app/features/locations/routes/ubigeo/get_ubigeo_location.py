
from typing import Annotated

from fastapi import Depends, Query

from app.features.locations.services.ubigeo_service import UbigeoService
from app.features.locations.schemas.ubigeo import UbigeoResponse

from app.features.locations.dependencies.services import get_ubigeo_service

from app.features.locations.ubigeo_router import router

@router.get("/ubigeo", response_model=UbigeoResponse)
async def get_ubigeo_by_location(
    service: Annotated[UbigeoService, Depends(get_ubigeo_service)],
    department: str = Query(min_length=1),
    province: str = Query(min_length=1),
    district: str = Query(min_length=1),
):
    ubigeo = await service.get_by_location(
        department=department,
        province=province,
        district=district,
    )

    return UbigeoResponse.model_validate(ubigeo)
