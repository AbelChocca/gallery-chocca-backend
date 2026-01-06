from app.modules.slide.domain.slide_entity import SlideEntity
from app.modules.slide.domain.dto import SlideFilterDTO
from app.infra.db.models.slide_model import SlideTable
from app.infra.db.mappers.slide_mapper import SlideMapper
from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.exceptions import DatabaseException

from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

class InfraSlideRepository(BaseRepository[SlideEntity, SlideTable]):
    async def get_slides_with_filter(
        self,
        slide_filters: SlideFilterDTO,
        offset: int = 0,
        limit: int = 20
    ) -> List[SlideEntity]:
        stmt = (
            select(SlideTable)
            .offset(offset)
            .limit(limit)
            .order_by(SlideTable.orden)
        )

        if slide_filters.activo is not None:
            stmt = stmt.where(SlideTable.activo == slide_filters.activo)

        if slide_filters.fecha_creada:
            stmt = stmt.where(SlideTable.fecha_creada >= slide_filters.fecha_creada)

        if slide_filters.fecha_actualizada:
            stmt = stmt.where(SlideTable.fecha_actualizada >= slide_filters.fecha_actualizada)

        try:
            result = await self.db_session.exec(stmt)
            slides = result.all()

            return [SlideMapper.to_entity(slide_db) for slide_db in slides]

        except SQLAlchemyError as e:
            raise DatabaseException("Database error while filtering slides.") from e