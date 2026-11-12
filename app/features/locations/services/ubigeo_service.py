
from app.features.locations.entities.ubigeo import Ubigeo
from app.features.locations.repositories.ubigeo_repository import (
    UbigeoRepository,
)

from app.core.exceptions import ValueNotFound

class UbigeoService:
    def __init__(
        self,
        ubigeo_repository: UbigeoRepository,
    ) -> None:
        self._ubigeo_repository = ubigeo_repository

    async def get_by_code(
        self,
        code: str,
    ) -> Ubigeo | None:
        return await self._ubigeo_repository.get_by_code(code)

    async def get_departments(self) -> list[str]:
        return await self._ubigeo_repository.get_departments()

    async def get_provinces(
        self,
        department: str,
    ) -> list[str]:
        return await self._ubigeo_repository.get_provinces(
            department=department,
        )

    async def get_districts(
        self,
        department: str,
        province: str,
    ) -> list[str]:
        return await self._ubigeo_repository.get_districts(
            department=department,
            province=province,
        )

    async def get_by_location(
        self,
        department: str,
        province: str,
        district: str,
    ) -> Ubigeo:
        ubigeo = await self._ubigeo_repository.get_by_location(
            department=department,
            province=province,
            district=district,
        )

        if not ubigeo:
            raise ValueNotFound(
                "No se encontro ubigeo seleccionado",
                {
                    "department": department,
                    "province": province,
                    "district": district
                }
            )

        return ubigeo
