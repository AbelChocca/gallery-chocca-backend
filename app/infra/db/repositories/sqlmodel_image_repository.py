from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_media import MediaImageTable
from app.domain.media.entities.image import ImageEntity
from app.infra.db.exceptions import DatabaseException, ModelNotFound

from sqlmodel import select, col
from sqlalchemy.exc import SQLAlchemyError

from typing import List, Optional

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
    
    async def get_images(
            self, 
            owner_type: str, 
            multiply: bool = False,
            owner_id: Optional[List[int] | int] = None
        ) -> List[ImageEntity] | ImageEntity:
        statement = (
            select(MediaImageTable)
            .where(MediaImageTable.owner_type == owner_type)
        )
        if multiply:
            statement = statement.where(col(MediaImageTable.owner_id).in_(owner_id or []))

            res: List[MediaImageTable] = (await self._db_session.exec(statement)).all()

            return [
                self._base_mapper.to_entity(image_table)
                for image_table in res
            ]
        statement = statement.where(col(MediaImageTable.owner_id == owner_id))

        res: MediaImageTable = (await self._db_session.exec(statement)).first()
        return self._base_mapper.to_entity(res)

    async def save_many(self, entities: List[ImageEntity]) -> List[ImageEntity]:
        try:
            models: List[MediaImageTable] = [self._base_mapper.to_db_model(entity) for entity in entities]

            self._db_session.add_all(models)
            await self._db_session.flush()
            await self._db_session.commit()
            return [self._base_mapper.to_entity(image_model) for image_model in models]
        except SQLAlchemyError as s:
            raise DatabaseException(f"Internal exception to save all the Image models: {str(s)}")