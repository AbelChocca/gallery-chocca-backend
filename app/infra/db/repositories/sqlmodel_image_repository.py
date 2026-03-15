from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_media import MediaImageTable
from app.domain.media.entities.image import ImageEntity
from app.domain.media.media_dto import ImageType
from app.infra.db.exceptions import DatabaseException

from sqlmodel import col
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from typing import List

class PostgresImageRepository(BaseRepository[ImageEntity, MediaImageTable]):
    async def delete_by_id(self, public_id: str) -> None:
        try:
            statement = delete(MediaImageTable).where(MediaImageTable.public_id == public_id)
            await self._db_session.execute(statement)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while deleting.",
                {
                    "repository": "postgres_image",
                    "event": "delete_by_id",
                    "model_db": MediaImageTable.__name__,
                    "public_id": public_id,
                }
                ) from s
    
    async def get_by_owner(
        self,
        *,
        owner_type: ImageType,
        owner_id: int
    ) -> List[ImageEntity]:
        stmt = (
            select(MediaImageTable)
            .where(MediaImageTable.owner_type == owner_type)
            .where(MediaImageTable.owner_id == owner_id)
        )

        res = (await self._db_session.execute(stmt)).scalars().all()

        return [
            self._base_mapper.to_entity(image)
            for image in res
        ]
    
    async def get_by_owners(
        self,
        *,
        owner_type: ImageType,
        owner_ids: List[int]
    ) -> List[ImageEntity]:
        if not owner_ids:
            return []

        stmt = (
            select(MediaImageTable)
            .where(MediaImageTable.owner_type == owner_type)
            .where(col(MediaImageTable.owner_id).in_(owner_ids))
        )

        res = (await self._db_session.execute(stmt)).scalars().all()

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

            return persisted_entities
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Internal exception to save all the Image models",
                {
                    "images_count": len(entities),
                    "event": "save_many",
                    "repository": "postgres_image"
                }
                ) from e
        
    async def delete_many_images(
            self, 
            owner_type: str,
            owner_ids: List[int]
    ) -> None:
        try:
            stmt = (
                delete(MediaImageTable)
                .where(MediaImageTable.owner_type == owner_type)
                .where(col(MediaImageTable.owner_id).in_(owner_ids))
            )

            await self._db_session.execute(stmt)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres delete failed",
                {
                    "service": "postgres/infra",
                    "repository": "postgres_image",
                    "event": "delete_many_images",
                    "owner_type": owner_type,
                    "owners_ids_sample": owner_ids[:5]
                }
            ) from s