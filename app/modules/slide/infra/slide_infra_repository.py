from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.slide_entity import SlideEntity
from app.modules.slide.infra.slide_model import SlideTable
from app.modules.slide.infra.slide_mapper import SlideMapper
from app.core.log.repository_logger import LoggerRepository
from app.shared.exceptions.domain.slide_exception import SlideNotFound
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException
from app.shared.dto.slide_dto import SlideFiltersDTO

from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

class InfraSlideRepository(SlideRepository):
    def __init__(
            self,
            db_session: AsyncSession,
            logger: LoggerRepository
            ):
        self.db_session = db_session
        self.logger = logger

    async def _get_by_id_non_raise(self, slide_id: int) -> Optional[SlideTable]:
        slide_db = await self.db_session.get(SlideTable, slide_id)
        return slide_db

    async def save(self, slide_entity: SlideEntity) -> SlideEntity:
        try:
            if slide_entity.id is None:
                slide_db = SlideMapper.to_db_model(slide_entity)
            else:
                # Update existing slide
                slide_db = SlideMapper.to_db_model(slide_entity, (await self._get_by_id_non_raise(slide_entity.id)))

            self.db_session.add(slide_db)
            await self.db_session.commit()
            await self.db_session.refresh(slide_db)

            return SlideMapper.to_entity(slide_db)

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            self.logger.error(f"Error while saving slide: {str(e)}")
            raise DatabaseException("Database error while saving slide.") from e

    async def delete_by_id(self, slide_id: int) -> None:
        try:
            slide_db = await self.db_session.get(SlideTable, slide_id)

            await self.db_session.delete(slide_db)
            await self.db_session.commit()

        except SlideNotFound as s:
            raise s
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException("Database error while deleting slide.") from e

    async def get_slides_with_filter(
        self,
        slide_filters: SlideFiltersDTO,
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

    async def get_by_id(self, slide_id: int) -> SlideEntity:
        try:
            slide_db = await self.db_session.get(SlideTable, slide_id)
            if not slide_db:
                raise SlideNotFound(f"Slide with id: {slide_id} not found")

            return slide_db
        except SQLAlchemyError as s:
            raise DatabaseException("Error during get slide by id") from s