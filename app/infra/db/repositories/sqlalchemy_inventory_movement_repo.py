from app.infra.db.repositories.base_repository import BaseRepository
from app.features.inventory.inventory_movement_entity import InventoryMovement
from app.infra.db.models.model_inventory_movement import InventoryMovementTable
from app.features.inventory.dto import InventoryMovementFilters
from sqlalchemy import select, func, Select, or_
from sqlmodel import col

class PostgresInventoryMovementReposity(BaseRepository[InventoryMovement, InventoryMovementTable]):
    async def count_with_filters(
        self,
        filters_command: InventoryMovementFilters | None = None
    ) -> int:
        stmt = select(func.count(InventoryMovementTable.id))
        if filters_command is not None:
            stmt = self._apply_filters(filters_command, stmt)

        result = await self._db_session.execute(stmt)

        return result.scalar() or 0

    async def get_with_filters(
        self,
        filters_command: InventoryMovementFilters,
        offset: int | None = None,
        limit: int | None = None
    ) -> list[InventoryMovement]:

        stmt = select(
            InventoryMovementTable
        )

        stmt = self._apply_filters(
            filters_command,
            stmt
        )

        stmt = stmt.order_by(
            col(
                InventoryMovementTable.created_at
            ).desc()
        )

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        results = await self._db_session.execute(
            stmt
        )

        movements = results.scalars().all()

        return [
            self._base_mapper.to_entity(
                movement
            )
            for movement in movements
        ]
    
    def _apply_filters(
        self,
        filters_command: InventoryMovementFilters,
        statement: Select[InventoryMovementTable]
    ) -> Select[InventoryMovementTable]:
        if filters_command.search:
            search = func.unaccent(f"%{filters_command.search}%")

            statement = statement.where(
                or_(
                    func.unaccent(col(InventoryMovementTable.owner_code)).ilike(search),
                    func.unaccent(col(InventoryMovementTable.owner_name)).ilike(search),
                )
            )

        if filters_command.from_date:
            statement = statement.where(
                InventoryMovementTable.created_at >= filters_command.from_date
            )

        if filters_command.to_date:
            statement = statement.where(
                InventoryMovementTable.created_at <= filters_command.to_date
            )

        if filters_command.type:
            statement = statement.where(
                InventoryMovementTable.type == filters_command.type
            )

        if filters_command.owner_id is not None:
            statement = statement.where(
                InventoryMovementTable.owner_id == filters_command.owner_id
            )

        if filters_command.owner_type is not None:
            statement = statement.where(
                InventoryMovementTable.owner_type == filters_command.owner_type
            )

        return statement