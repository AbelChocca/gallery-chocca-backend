from app.infra.db.repositories.base_repository import BaseRepository
from app.modules.user.domain.user import User
from app.modules.user.domain.user_exception import UserNotFoundException
from app.infra.db.models.model_user import UserTable
from app.infra.db.mappers.user_mapper import UserMapper
from app.core.log.logger_repository import LoggerProtocol

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

class PostgresUserRepository(BaseRepository[User, UserTable]):
    def __init__(
            self, 
            db_session: AsyncSession,
            logger: LoggerProtocol
            ):
        self.db_session = db_session
        self.logger = logger

    async def get_by_email(self, email: str) -> User:
        statement = select(UserTable).where(UserTable.email == email)
        user_db = (await self.db_session.exec(statement)).first()
        if not user_db:
            raise UserNotFoundException(f"User with email={email} not found")
        return UserMapper.to_entity(user_db)