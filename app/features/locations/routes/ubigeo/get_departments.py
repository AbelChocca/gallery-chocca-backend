
from typing import Annotated

from fastapi import Depends

from app.features.locations.services.ubigeo_service import UbigeoService
from app.features.locations.dependencies.services import get_ubigeo_service

from app.features.locations.ubigeo_router import router

@router.get("/departments", response_model=list[str])
async def get_departments(
    service: Annotated[UbigeoService, Depends(get_ubigeo_service)],
):
    return await service.get_departments()
