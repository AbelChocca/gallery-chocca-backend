from sqlalchemy import select, or_, func

from app.features.locations.entities.location import Location
from app.features.locations.models.locations import LocationTable
from app.features.locations.types import LocationType

from app.infra.db.repositories.base_repository import BaseRepository

class LocationRepository(BaseRepository[Location, LocationTable]):

    async def get_by_name(
        self,
        name: str,
    ) -> Location | None:
        stmt = (
            select(LocationTable)
            .where(
                func.lower(func.trim(LocationTable.name))
                == name.strip().lower()
            )
            .limit(1)
        )

        result = await self._db_session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._base_mapper.to_entity(model)

    async def get_inventory_locations(
        self,
        *,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> list[Location]:

        allowed_types = (
            LocationType.STORE,
            LocationType.WORKSHOP,
            LocationType.WAREHOUSE,
        )

        stmt = select(LocationTable).where(
            LocationTable.type.in_(allowed_types)
        )

        if search:
            stmt = stmt.where(
                LocationTable.name.ilike(f"%{search.strip()}%")
            )

        if is_active is not None:
            stmt = stmt.where(
                LocationTable.is_active == is_active
            )

        stmt = stmt.order_by(LocationTable.name.asc())

        result = await self._db_session.execute(stmt)

        locations = result.scalars().all()

        return [
            self._base_mapper.to_entity(location)
            for location in locations
        ]

    async def get_locations(
        self,
        *,
        search: str | None = None,
        location_type: LocationType | None = None,
        is_active: bool | None = None,
        pickup_enabled: bool | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Location], int]:

        conditions = []

        if location_type is not None:
            conditions.append(
                LocationTable.type == location_type
            )

        if is_active is not None:
            conditions.append(
                LocationTable.is_active.is_(is_active)
            )

        if pickup_enabled is not None:
            conditions.append(
                LocationTable.pickup_enabled.is_(
                    pickup_enabled
                )
            )

        if search and search.strip():
            pattern = f"%{search.strip()}%"

            conditions.append(
                or_(
                    LocationTable.name.ilike(pattern),
                    LocationTable.address.ilike(pattern),
                    LocationTable.reference.ilike(pattern),
                )
            )

        count_statement = (
            select(func.count(LocationTable.id))
            .where(*conditions)
        )

        total_items = (
            await self._db_session.scalar(count_statement)
        ) or 0

        statement = (
            select(LocationTable)
            .where(*conditions)
            .order_by(
                LocationTable.name.asc(),
                LocationTable.id.asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.execute(statement)

        locations = [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

        return locations, total_items

    async def get_pickup_locations(self) -> list[Location]:

        statement = (
            select(LocationTable)
            .where(
                LocationTable.type == LocationType.STORE,
                LocationTable.is_active.is_(True),
                LocationTable.pickup_enabled.is_(True),
                LocationTable.address.is_not(None),
                LocationTable.address != "",
                LocationTable.ubigeo_code.is_not(None),
                LocationTable.ubigeo_code != "",
            )
            .order_by(
                LocationTable.name.asc(),
                LocationTable.id.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]
