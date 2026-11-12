
from sqlalchemy import select

from app.features.locations.entities.ubigeo import Ubigeo
from app.features.locations.models.ubigeo import UbigeoTable
from app.infra.db.repositories.base_repository import BaseRepository


class UbigeoRepository(
    BaseRepository[Ubigeo, UbigeoTable],
):
    async def get_by_code(
        self,
        code: str,
    ) -> Ubigeo | None:
        stmt = select(UbigeoTable).where(
            UbigeoTable.code == code,
        )

        result = await self._db_session.execute(stmt)
        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model is not None
            else None
        )

    async def get_departments(self) -> list[str]:
        stmt = (
            select(UbigeoTable.department)
            .distinct()
            .order_by(UbigeoTable.department)
        )

        result = await self._db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_provinces(
        self,
        department: str,
    ) -> list[str]:
        stmt = (
            select(UbigeoTable.province)
            .where(
                UbigeoTable.department == department,
            )
            .distinct()
            .order_by(UbigeoTable.province)
        )

        result = await self._db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_districts(
        self,
        department: str,
        province: str,
    ) -> list[str]:
        stmt = (
            select(UbigeoTable.district)
            .where(
                UbigeoTable.department == department,
                UbigeoTable.province == province,
            )
            .distinct()
            .order_by(UbigeoTable.district)
        )

        result = await self._db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_location(
        self,
        department: str,
        province: str,
        district: str,
    ) -> Ubigeo | None:
        stmt = (
            select(UbigeoTable)
            .where(
                UbigeoTable.department == department,
                UbigeoTable.province == province,
                UbigeoTable.district == district,
            )
            .order_by(UbigeoTable.code)
            .limit(1)
        )

        result = await self._db_session.execute(stmt)
        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model is not None
            else None
        )
