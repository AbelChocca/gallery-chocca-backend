from app.infra.db.repositories.base_repository import BaseRepository
from app.domain.inventory.inventory_movement_entity import InventoryMovement
from app.infra.db.models.model_inventory_movement import InventoryMovementTable
from app.infra.db.models.model_product import VariantSizeTable
from app.domain.inventory.data_models import InventoryMovementFilters
from sqlalchemy import select, func, Select
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
        offset: int,
        limit: int
    ) -> list[InventoryMovement]:
        stmt = select(InventoryMovementTable)

        stmt = self._apply_filters(filters_command, stmt)
        stmt = stmt.order_by(col(InventoryMovementTable.created_at).asc()).offset(offset).limit(limit)

        results = await self._db_session.execute(stmt)

        movements = results.scalars().all()

        return [
            self._base_mapper.to_entity(movement)
            for movement in movements
        ]
    
    def _apply_filters(
            self,
            filters_command: InventoryMovementFilters,
            statement: Select[InventoryMovementTable]
    ) -> Select[InventoryMovementTable]:
        if filters_command.sku is not None:
            statement = statement.join(
                VariantSizeTable,
                VariantSizeTable.id == InventoryMovementTable.variant_size_id
            ).where(VariantSizeTable.sku == filters_command.sku)

        if filters_command.from_date:
            statement = statement.where(InventoryMovementTable.created_at >= filters_command.from_date)

        if filters_command.to_date:
            statement = statement.where(InventoryMovementTable.created_at <= filters_command.to_date)

        if filters_command.type:
            statement = statement.where(InventoryMovementTable.type == filters_command.type)
            
        return statement