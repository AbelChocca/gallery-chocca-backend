from typing import Generic, Type
from app.infra.db.types import E, M
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.infra.db.mappers.base_mapper import BaseMapper

from app.infra.db.exceptions import DatabaseException
from app.core.exceptions import ValueNotFound

class BaseRepository(Generic[E, M]):
    def __init__(
            self,
            db_session: AsyncSession,
            base_mapper: BaseMapper[E, M],
            base_model: Type[M]
        ):
        self._db_session: AsyncSession = db_session
        self._base_model: Type[M] = base_model
        self._base_mapper: BaseMapper[E, M] = base_mapper

    async def _get_model_by_id_non_raise(self, model_id: int) -> M | None:
        statement = (
            select(self._base_model)
            .where(self._base_model.id == model_id)
        )
        
        result = await self._db_session.execute(statement)
        model: M | None = result.scalar()
        if not model:
            return None
        
        return model

    async def save(self, entity: E) -> E:
        try:
            if entity.id is None:
                model: M = self._base_mapper.to_db_model(entity)
            else:
                model: M = self._base_mapper.to_db_model(entity=entity, existing_model=(await self._get_model_by_id_non_raise(entity.id)))

            self._db_session.add(model)
            await self._db_session.flush()

            return self._base_mapper.to_entity(model)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while saving",
                {
                    "repository": f"postgres_{E.__name__.lower()}",
                    "base_model": self._base_model.__name__,
                    "event": "save"
                }
                ) from s
        
    async def delete_by_id(self, model_id: int) -> None:
        try:
            stmt = delete(self._base_model).where(self._base_model.id == model_id)

            await self._db_session.execute(stmt)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while deleting.",
                {
                    "repository": f"postgres_{E.__name__.lower()}",
                    "base_model": self._base_model.__name__,
                    "event": "delete_by_id",
                    "model_id": model_id
                }
            ) from s
        
    async def get_by_id(self, model_id: int, raises: bool = True) -> E | None:
        try:
            model_db = await self._get_model_by_id_non_raise(model_id)
            if not model_db:
                if not raises:
                    return None

                raise ValueNotFound(
                    "Model wasn't found.",
                    {
                        "repository": f"postres_{E.__name__.lower()}",
                        "base_model": self._base_model.__name__,
                        "event": "get_by_id",
                        "model_id": model_id
                    }
                    )

            return self._base_mapper.to_entity(model_db)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting.",
                {
                    "repository": f"postgres_{E.__name__.lower()}",
                    "base_model": self._base_model.__name__,
                    "event": "get_by_id",
                    "model_id": model_id
                }
            ) from s