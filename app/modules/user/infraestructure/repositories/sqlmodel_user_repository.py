from app.modules.user.domain.repository_user import UserRepository
from app.modules.user.domain.user import User
from app.shared.exceptions.infraestructure_exception import DatabaseException
from app.modules.user.domain.user_exception import UserNotFoundException
from app.modules.user.infraestructure.models.model_user import UserTable
from app.modules.user.infraestructure.user_mapper import UserMapper
from app.core.log.logger_repository import LoggerRepository

from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

class PostgresUserRepository(UserRepository):
    def __init__(
            self, 
            db_session: AsyncSession,
            logger: LoggerRepository
            ):
        self.db_session = db_session
        self.logger = logger

    async def _get_user_table_or_none(self, id:int) -> Optional[UserTable]:
        return await self.db_session.get(UserTable, id)
    
    async def _get_user_table_or_raise(self, id: int) -> UserTable:
        user_db = await self.db_session.get(UserTable, id)
        if not user_db:
            raise UserNotFoundException(f"User with id={id} not found")
        return user_db

    async def get_by_id(self, id: int) -> Optional[User]:
        user_db = await self._get_user_table_or_none(id)
        return UserMapper.to_entity(user_db) if user_db else None

    async def get_by_email(self, email: str) -> User:
        statement = select(UserTable).where(UserTable.email == email)
        user_db = (await self.db_session.exec(statement)).first()
        if not user_db:
            raise UserNotFoundException(f"User with email={email} not found")
        return UserMapper.to_entity(user_db)

    async def save(self, user: User) -> User:
        try:
            existing = None
            if user.id is not None:
                existing = await self._get_user_table_or_none(user.id)
            user_db = UserMapper.to_db_model(user, existing)

            self.db_session.add(user_db)
            await self.db_session.commit()
            await self.db_session.refresh(user_db)

            return UserMapper.to_entity(user_db)
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            self.logger.error(f"Internal's error to save user to database: {str(e)}")
            raise DatabaseException("Could not save user to database") from e

    async def delete_by_id(self, id: int) -> None:
        try:
            user_db = await self._get_user_table_or_raise(id)
            await self.db_session.delete(user_db)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException("Database operation failed") from e