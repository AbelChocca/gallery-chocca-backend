from app.domain.slide.slide_entity import SlideEntity
from app.domain.slide.slide_dto import SlideFiltersCommand
from app.infra.db.models.model_slide import SlideTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.exceptions import DatabaseException

from typing import List, Dict
from sqlalchemy import case, update, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import col
from sqlmodel.sql.expression import SelectOfScalar, Select
import random

OFFSET = 1_000_000

class PostgresSlideRepository(BaseRepository[SlideEntity, SlideTable]):
    def _apply_filter(
            self,
            *,
            statement: Select[SlideTable] | SelectOfScalar[SlideTable],
            slide_filters: SlideFiltersCommand
    ) -> Select[SlideTable] | SelectOfScalar[SlideTable]:
        
        if slide_filters.activo is not None:
            statement = statement.where(col(SlideTable.activo).is_(slide_filters.activo))

        if slide_filters.fecha_creada is not None:
            statement = statement.where(SlideTable.fecha_creada >= slide_filters.fecha_creada)

        if slide_filters.fecha_actualizada is not None:
            statement = statement.where(SlideTable.fecha_actualizada >= slide_filters.fecha_actualizada)

        return statement
    
    async def _get_last_order(self) -> int:
        return (await self.count_all(SlideFiltersCommand(activo=True))) + 1

    async def count_slides_by_active_session(self) -> list[tuple[bool, int]]:
        stmt = select(SlideTable.activo, func.count()).group_by(SlideTable.activo)

        res = await self._db_session.execute(stmt)

        slides_by_active_session: list[tuple[bool, int]] = res.all()
        return slides_by_active_session
    
    async def get_last_n_slides(self, n: int) -> list[SlideEntity]:
        stmt = select(SlideTable).order_by(col(SlideTable.id).desc()).limit(n)

        res = await self._db_session.execute(stmt)

        slides = res.scalars().all()
        return [
            self._base_mapper.to_entity(slide)
            for slide in slides
        ]

    async def count_all(
            self,
            slide_filters: SlideFiltersCommand | None = None
    ) -> int:
        stmt = select(func.count(SlideTable.id))
        if slide_filters is not None:
            stmt = self._apply_filter(
                statement=stmt,
                slide_filters=slide_filters
            )

        res = await self._db_session.execute(stmt)
        return res.scalar() or 0
    
    async def toggle_slide_session(
            self,
            slide_id: int,
            is_active: bool
    ) -> None:
        try:
            stmt = (
                update(SlideTable)
                .where(SlideTable.id == slide_id)
                .values(activo=is_active)
            )
            if not is_active:
                stmt = stmt.values(orden=random.randint(999, 9_999)) 
            else:
                stmt = stmt.values(orden=await self._get_last_order())

            await self._db_session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseException(
                f"{e._message()}",
                {
                    "event": "toggle_slide_session",
                    "slide_id": slide_id,
                    "toggle_session": is_active,
                    "cause": f"{getattr(e.__cause__, "args", e.__cause__)}"
                }
            ) from e
    async def update_many_orders(
        self,
        ids: List[int],
        updates: List[Dict[str, int]]
    ) -> None:
        try: 
            await self._db_session.execute(
                update(SlideTable)
                .where(
                    col(SlideTable.id).in_(ids),
                    col(SlideTable.activo).is_(True)
                )
                .values(orden=SlideTable.orden + OFFSET)
            )

            case_stmt = case(
                {upd["b_id"]: upd["new_order"] for upd in updates},
                value=SlideTable.id
            )

            await self._db_session.execute(
                update(SlideTable)
                .where(col(SlideTable.id).in_(ids), SlideTable.activo.is_(True))
                .values(orden=case_stmt)
            )
        except SQLAlchemyError as e:
            raise DatabaseException(
                f"{e._message()}",
                {
                    "event": "update_many_orders",
                    "slide_ids_count": len(ids),
                    "slide_ids_sample": ids[:5],
                    "cause": f"{getattr(e.__cause__, "args", e.__cause__)}"
                }
            ) from e
        
    async def get_slides_with_filter(
        self,
        slide_filters: SlideFiltersCommand,
        offset: int = 0,
        limit: int = 20
    ) -> List[SlideEntity]:
        stmt = select(SlideTable)

        stmt = self._apply_filter(
            statement=stmt,
            slide_filters=slide_filters
        )
        stmt = (
            stmt
            .order_by(col(SlideTable.orden).asc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await self._db_session.execute(stmt)
        slides = result.scalars().all()

        return [self._base_mapper.to_entity(slide_db) for slide_db in slides]