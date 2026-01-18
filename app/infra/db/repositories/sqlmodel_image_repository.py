from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_media import MediaImageTable
from app.domain.media.entities.image import ImageEntity
from app.infra.db.exceptions import DatabaseException, ModelNotFound

from sqlmodel import select, col
from sqlalchemy.exc import SQLAlchemyError

from typing import List

class PostgresImageRepository(BaseRepository[ImageEntity, MediaImageTable]):
    async def delete_by_id(self, model_id: str):
        try:
            statement = select(MediaImageTable).where(MediaImageTable.service_id == model_id)
            model_db = await self._db_session.exec(statement)

            if not model_db:
                raise ModelNotFound(f"Model {MediaImageTable.__name__} with id: {model_id} wasn't found, cannot deleted.")

            await self._db_session.delete(model_db)
            await self._db_session.commit()
        except SQLAlchemyError as s:
            await self._db_session.rollback()
            raise DatabaseException(f"Database error while deleting {MediaImageTable.__name__}.") from s
    
    async def get_by_owner(
        self,
        *,
        owner_type: str,
        owner_id: int
    ) -> List[ImageEntity]:
        stmt = (
            select(MediaImageTable)
            .where(MediaImageTable.owner_type == owner_type)
            .where(MediaImageTable.owner_id == owner_id)
        )

        res = (await self._db_session.exec(stmt)).all()

        return [
            self._base_mapper.to_entity(image)
            for image in res
        ]
    
    async def get_by_owners(
        self,
        *,
        owner_type: str,
        owner_ids: List[int]
    ) -> List[ImageEntity]:
        if not owner_ids:
            return []

        stmt = (
            select(MediaImageTable)
            .where(MediaImageTable.owner_type == owner_type)
            .where(col(MediaImageTable.owner_id).in_(owner_ids))
        )

        res = (await self._db_session.exec(stmt)).all()

        return [
            self._base_mapper.to_entity(image)
            for image in res
        ]

    async def save_many(self, entities: List[ImageEntity]) -> List[ImageEntity]:
        try:
            models: List[MediaImageTable] = [self._base_mapper.to_db_model(entity) for entity in entities]

            self._db_session.add_all(models)
            await self._db_session.flush()
            persisted_entities = [self._base_mapper.to_entity(image_model) for image_model in models]

            await self._db_session.commit()
            return persisted_entities
        except SQLAlchemyError as s:
            raise DatabaseException(f"Internal exception to save all the Image models: {str(s)}")