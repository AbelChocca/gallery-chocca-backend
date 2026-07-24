from sqlalchemy import select, update

from app.features.inventory.entities.inventory_location import InventoryLocation
from app.features.inventory.models.inventory_location import InventoryLocationTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.features.inventory.types.inventory_location import InventoryLocationType


class InventoryLocationRepository(
    BaseRepository[InventoryLocation, InventoryLocationTable]
):
    
    async def get_locations(
        self,
        *,
        search: str | None = None,
        is_active: bool | None = None,
        location_type: InventoryLocationType | None = None,
    ) -> list[InventoryLocation]:

        statement = select(InventoryLocationTable)

        if search:
            statement = statement.where(
                InventoryLocationTable.name.ilike(f"%{search}%")
            )

        if is_active is not None:
            statement = statement.where(
                InventoryLocationTable.is_active.is_(is_active)
            )

        if location_type is not None:
            statement = statement.where(
                InventoryLocationTable.type == location_type
            )

        statement = statement.order_by(
            InventoryLocationTable.name.asc()
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def get_active_locations(
        self,
    ) -> list[InventoryLocation]:

        statement = (
            select(InventoryLocationTable)
            .where(
                InventoryLocationTable.is_active.is_(True)
            )
            .order_by(
                InventoryLocationTable.name.asc()
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def get_by_id(
        self,
        location_id: int,
    ) -> InventoryLocation | None:

        statement = (
            select(InventoryLocationTable)
            .where(
                InventoryLocationTable.id == location_id
            )
        )

        result = await self._db_session.execute(statement)

        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model
            else None
        )

    async def get_by_name(
        self,
        name: str,
    ) -> InventoryLocation | None:

        statement = (
            select(InventoryLocationTable)
            .where(
                InventoryLocationTable.name == name
            )
        )

        result = await self._db_session.execute(statement)

        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model
            else None
        )

    async def get_by_name_except_id(
        self,
        *,
        name: str,
        location_id: int,
    ) -> InventoryLocation | None:

        statement = (
            select(InventoryLocationTable)
            .where(
                InventoryLocationTable.name == name,
                InventoryLocationTable.id != location_id,
            )
        )

        result = await self._db_session.execute(statement)

        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model
            else None
        )
    
    async def toggle_status(
        self,
        *,
        location_id: int,
        is_active: bool,
    ) -> None:

        statement = (
            update(InventoryLocationTable)
            .where(
                InventoryLocationTable.id == location_id
            )
            .values(
                is_active=is_active,
            )
        )

        await self._db_session.execute(statement)