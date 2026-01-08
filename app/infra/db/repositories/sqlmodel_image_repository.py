from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_media import MediaImageTable
from app.domain.media.entities.image import ImageEntity
from app.infra.db.exceptions import DatabaseException

from sqlmodel import select, col
from sqlalchemy.exc import SQLAlchemyError

from typing import List, Optional

class PostgresImageRepository(BaseRepository[ImageEntity, MediaImageTable]):
    async def get_images(self, owner_type: str, owners_id: Optional[List[int]] = None) -> List[ImageEntity]:
        statement = (
            select(MediaImageTable)
            .where(MediaImageTable.owner_type == owner_type)
        )
        if owners_id is not None:
            statement = statement.where(col(MediaImageTable.owner_id).in_(owners_id))

        res: List[MediaImageTable] = (await self._db_session.exec(statement)).all()

        return [
            self._base_mapper.to_entity(image_table)
            for image_table in res
        ]
    async def save_many(self, entities: List[ImageEntity]) -> List[ImageEntity]:
        try:
            models: List[MediaImageTable] = [self._base_mapper.to_db_model(entity) for entity in entities]

            self._db_session.add_all(models)
            await self._db_session.flush()
            await self._db_session.commit()
            return [self._base_mapper.to_entity(image_model) for image_model in models]
        except SQLAlchemyError as s:
            raise DatabaseException(f"Internal exception to save all the Image models: {str(s)}")