from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Generic, Optional, Type
from app.infra.db.types import E, M
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

from app.infra.db.mappers.base_mapper import BaseMapper
from app.core.log.protocole import LoggerProtocol

from app.infra.db.exceptions import DatabaseException, ModelNotFound

class BaseRepository(Generic[E, M]):
    def __init__(
            self,
            db_session: AsyncSession,
            base_mapper: BaseMapper[E, M],
            logger: LoggerProtocol,
            base_model: Type[M]
        ):
        self._db_session: AsyncSession = db_session
        self._base_model: Type[M] = base_model
        self._base_mapper: BaseMapper[E, M] = base_mapper
        self._logger: LoggerProtocol= logger

    async def _get_model_by_id_non_raise(self, model_id: int) -> Optional[M]:
        statement = (
            select(self._base_model)
            .where(self._base_model.id == model_id)
        )
        
        model: Optional[M] = (await self._db_session.exec(statement)).first()
        if not model:
            self._logger.warning(
                f"Model {self._base_model.__name__} with id: {model_id} wasn't found.",
                service="infra/db"
            )
            return None
        
        return model

    async def save(self, entity: E) -> E:
        try:
            if entity.id is None:
                model: M = self._base_mapper.to_db_model(entity)
            else:
                model: M = self._base_mapper.to_db_model(entity=entity, existing_model=(await self._get_model_by_id_non_raise(entity.id)))

            self._db_session.add(model)
            await self._db_session.commit()
            await self._db_session.refresh(model)
            return self._base_mapper.to_entity(model)
        except SQLAlchemyError as s:
            await self._db_session.rollback()
            self._logger.error(f"Error while saving {self._base_model.__name__}: {str(s)}")
            raise DatabaseException(f"Database error while saving {self._base_model.__name__}.") from s
        
    async def delete_by_id(self, model_id: int) -> None:
        try:
            model_db = await self._get_model_by_id_non_raise(model_id)

            if not model_db:
                raise ModelNotFound(f"Model {self._base_model.__name__} with id: {model_id} wasn't found, cannot deleted.")

            await self._db_session.delete(model_db)
            await self._db_session.commit()
        except SQLAlchemyError as s:
            await self._db_session.rollback()
            raise DatabaseException(f"Database error while deleting {self._base_model.__name__}.") from s
        
    async def get_by_id(self, model_id: int, raises: bool = True) -> Optional[E]:
        try:
            model_db = await self._get_model_by_id_non_raise(model_id)
            if not model_db:
                if not raises:
                    return None

                raise ModelNotFound(f"Model {self._base_model.__name__} with id: {model_id} not found")

            return self._base_mapper.to_entity(model_db)
        except SQLAlchemyError as s:
            raise DatabaseException(f"Error during get {self._base_model.__name__} by id") from s