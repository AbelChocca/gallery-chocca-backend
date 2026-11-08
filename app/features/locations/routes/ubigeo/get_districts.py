
from typing import Annotated

from fastapi import Depends, Query

from app.features.locations.services.ubigeo_service import UbigeoService
from app.features.locations.dependencies.services import get_ubigeo_service

from app.features.locations.ubigeo_router import router

@router.get("/districts", response_model=list[str])
async def get_districts(
    service: Annotated[UbigeoService, Depends(get_ubigeo_service)],
    department: str = Query(min_length=1),
    province: str = Query(min_length=1),
):
    return await service.get_districts(
        department=department,
        province=province,
    )

