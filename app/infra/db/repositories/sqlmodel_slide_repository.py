from app.domain.slide.slide_entity import SlideEntity
from app.domain.slide.slide_dto import SlideFilterDTO
from app.infra.db.models.model_slide import SlideTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.exceptions import DatabaseException

from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, col, func, update, text
from sqlmodel.sql.expression import SelectOfScalar, Select

OFFSET = 1_000_000

class PostgresSlideRepository(BaseRepository[SlideEntity, SlideTable]):
    def _apply_filter(
            self,
            *,
            statement: Select[SlideTable] | SelectOfScalar[SlideTable],
            slide_filters: SlideFilterDTO
    ) -> Select[SlideTable] | SelectOfScalar[SlideTable]:
        
        if slide_filters.activo is not None:
            statement = statement.where(col(SlideTable.activo).is_(slide_filters.activo))

        if slide_filters.fecha_creada is not None:
            statement = statement.where(SlideTable.fecha_creada >= slide_filters.fecha_creada)

        if slide_filters.fecha_actualizada is not None:
            statement = statement.where(SlideTable.fecha_actualizada >= slide_filters.fecha_actualizada)

        return statement

    async def count_all(
            self,
            slide_filters: SlideFilterDTO
    ) -> int:
        stmt = select(func.count(SlideTable.id))
        stmt = self._apply_filter(
            statement=stmt,
            slide_filters=slide_filters
        )

        res = await self._db_session.exec(stmt)
        return res.one() or 0
    
    async def update_many_orders(
        self,
        ids: List[int],
        updates: List[Dict[str, int]]
    ) -> None:
        try: 
            await self._db_session.exec(
                update(SlideTable)
                .where(
                    col(SlideTable.id).in_(ids),
                    col(SlideTable.activo).is_(True)
                )
                .values(orden=SlideTable.orden + OFFSET)
            )

            stmt = text("""
                UPDATE slide
                SET orden = :new_order
                WHERE id = :b_id AND activo = true
            """)

            await self._db_session.exec(stmt, params=updates)
            await self._db_session.commit()
        except SQLAlchemyError as e:
            await self._db_session.rollback()
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
        slide_filters: SlideFilterDTO,
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
        
        result = await self._db_session.exec(stmt)
        slides = result.all()

        return [self._base_mapper.to_entity(slide_db) for slide_db in slides]