from sqlmodel import select, col
from sqlalchemy import or_, Select, func, and_, case, update, delete
from sqlalchemy.orm import selectinload

from app.features.material.entities.material import Material
from app.features.material.models.model_material import MaterialTable, MaterialComponentTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.features.material.dto.material import MaterialFilters
from app.features.inventory.types.inventory import AvailabilityStatus

from app.core.exceptions import ValueNotFound
from decimal import Decimal


class PostgresMaterialRepository(
    BaseRepository[Material, MaterialTable]
):
    async def get_components_by_material_id(
        self,
        *,
        material_id: int,
    ) -> list[MaterialComponentTable]:

        statement = (
            select(
                MaterialComponentTable
            )
            .where(
                MaterialComponentTable.material_id ==
                material_id
            )
            .order_by(
                MaterialComponentTable.id.asc()
            )
        )


        result = await self._db_session.execute(
            statement
        )

        return result.scalars().all()
    
    async def delete_components_by_material_id(
        self,
        material_id: int
    ) -> None:
        statement = (
            delete(MaterialComponentTable)
            .where(
                MaterialComponentTable.material_id == material_id
            )
        )

        await self._db_session.execute(statement)
        
    async def get_by_id(
        self,
        material_id: int,
    ) -> Material | None:
        statement = (
            select(MaterialTable)
            .where(
                MaterialTable.id == material_id
            )
            .options(
                selectinload(
                    MaterialTable.components
                )
            )
        )

        result = await self._db_session.execute(statement)

        material = result.scalar_one_or_none()

        if not material:
            raise ValueNotFound(
                "Material wasn't found.",
                {
                    "repository": "material",
                    "base_model": self._base_model.__name__,
                    "event": "get_by_id",
                    "material_id": material_id
                }
            )
        
        return self._base_mapper.to_entity(material)
    
    async def get_by_code(
        self,
        code: str
    ) -> Material:
        statement = (
            select(MaterialTable)
            .where(MaterialTable.code == code)
        )

        material_db = (
            await self._db_session.execute(statement)
        ).scalar_one_or_none()

        if not material_db:
            raise ValueNotFound(
                "Material not found.",
                {
                    "repository": "postgres_material",
                    "event": "get_by_code",
                    "code": code
                }
            )

        return self._base_mapper.to_entity(material_db)
    
    async def get_by_ids(
        self,
        ids: list[int]
    ) -> list[Material]:

        if not ids:
            return []

        statement = (
            select(MaterialTable)
            .where(
                col(MaterialTable.id).in_(ids)
            )
        )

        materials_db = (
            await self._db_session.execute(statement)
        ).scalars().all()

        return [
            self._base_mapper.to_entity(material)
            for material in materials_db
        ]
    
    async def update_stock(
        self,
        material_id: int,
        new_stock: Decimal
    ) -> None:

        await self._db_session.execute(
            update(MaterialTable)
            .where(
                MaterialTable.id == material_id
            )
            .values(
                stock=new_stock
            )
        )
    
    async def update_stock_many(
        self,
        stock_updates: dict[int, Decimal]
    ) -> None:

        await self._db_session.execute(
            update(MaterialTable)
            .where(
                col(MaterialTable.id).in_(stock_updates.keys())
            )
            .values(
                stock=case(
                    stock_updates,
                    value=MaterialTable.id
                )
            )
        )

    async def exists_by_code(
        self,
        code: str
    ) -> bool:
        statement = (
            select(MaterialTable.id)
            .where(MaterialTable.code == code)
        )

        return (
            await self._db_session.execute(statement)
        ).scalar_one_or_none() is not None

    async def exists_by_name(
        self,
        name: str
    ) -> bool:
        statement = (
            select(MaterialTable.id)
            .where(
                col(MaterialTable.name) == name
            )
        )

        return (
            await self._db_session.execute(statement)
        ).scalar_one_or_none() is not None
    
    async def count_all(
        self,
        *,
        filters: MaterialFilters | None = None,
    ) -> int:

        statement = select(
            func.count(MaterialTable.id)
        )

        if filters:
            statement = self._apply_filters(
                statement,
                filters=filters
            )

        return (
            await self._db_session.execute(statement)
        ).scalar_one()

    async def get_all(
        self,
        *,
        filters: MaterialFilters | None = None,
        offset: int = 0,
        limit: int = 20
    ) -> list[Material]:
        statement = select(MaterialTable)
        
        if filters:
            statement = self._apply_filters(
                statement,
                filters=filters
            )

        statement = (
            statement
            .order_by(
                col(MaterialTable.created_at).desc(),
                col(MaterialTable.id).desc()
            )
            .offset(offset)
            .limit(limit)
        )

        materials = (
            await self._db_session.execute(statement)
        ).scalars().all()

        return [
            self._base_mapper.to_entity(material)
            for material in materials
        ]
    
    def _apply_filters(
        self,
        statement: Select,
        *,
        filters: MaterialFilters,
    ) -> Select:

        if filters.search:
            search = func.unaccent(f"%{filters.search}%")

            statement = statement.where(
                or_(
                    func.unaccent(col(MaterialTable.code)).ilike(search),
                    func.unaccent(col(MaterialTable.name)).ilike(search),
                )
            )

        if filters.company:
            statement = statement.where(
                MaterialTable.company == filters.company
            )

        if filters.material_type:
            statement = statement.where(
                MaterialTable.material_type == filters.material_type
            )

        if filters.is_active is not None:
            statement = statement.where(
                MaterialTable.is_active == filters.is_active
            )

        return statement