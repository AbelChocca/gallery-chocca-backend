from app.infra.db.repositories.base_repository import BaseRepository
from app.features.inventory.entities.inventory_movement_entity import InventoryMovement
from app.features.inventory.models.inventory_movement import InventoryMovementTable
from app.features.inventory.dtos.inventory_movements import InventoryMovementFilters, InventoryMovementSummaryDTO
from app.features.inventory.types.inventory_movement import InventoryOwnerType, InventoryMovementType
from sqlalchemy import select, func, Select, or_, case
from sqlmodel import col
from decimal import Decimal

class PostgresInventoryMovementReposity(BaseRepository[InventoryMovement, InventoryMovementTable]):
    async def get_last_material_movement(
        self,
        owner_type: InventoryOwnerType,
        owner_id: int
    ) -> InventoryMovement:
        stmt = (
            select(InventoryMovementTable)
            .where(
                InventoryMovementTable.owner_type == owner_type,
                InventoryMovementTable.owner_id == owner_id
            )
            .order_by(
                col(InventoryMovementTable.created_at).desc()
            )
        )

        result = await self._db_session.execute(stmt)

        movement = result.scalars().first()

        return movement

    async def get_last_movements_by_owner_ids(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_ids: list[int],
    ) -> dict[int, InventoryMovement]:

        if not owner_ids:
            return {}

        stmt = (
            select(InventoryMovementTable)
            .where(
                InventoryMovementTable.owner_type == owner_type,
                InventoryMovementTable.owner_id.in_(owner_ids),
            )
            .distinct(
                InventoryMovementTable.owner_id,
            )
            .order_by(
                InventoryMovementTable.owner_id,
                col(InventoryMovementTable.created_at).desc(),
            )
        )

        result = await self._db_session.execute(stmt)

        movements = result.scalars().all()

        return {
            movement.owner_id: movement
            for movement in movements
        }
        
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

    async def get_movement_summary(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_ids: list[int],
        location_id: int,
    ) -> InventoryMovementSummaryDTO:
        if not owner_ids:
            return InventoryMovementSummaryDTO(
                total_entries=0,
                total_exits=0,
            )

        stmt = (
            select(
                func.count(
                    case(
                        (
                            InventoryMovementTable.type
                            == InventoryMovementType.ENTRY,
                            1,
                        )
                    )
                ).label("total_entries"),
                func.count(
                    case(
                        (
                            InventoryMovementTable.type
                            == InventoryMovementType.USAGE,
                            1,
                        )
                    )
                ).label("total_exits"),
            )
            .where(
                InventoryMovementTable.owner_type == owner_type,
                InventoryMovementTable.owner_id.in_(owner_ids),
                InventoryMovementTable.location_id == location_id,
            )
        )

        result = await self._db_session.execute(stmt)
        row = result.one()

        return InventoryMovementSummaryDTO(
            total_entries=row.total_entries,
            total_exits=row.total_exits,
        )