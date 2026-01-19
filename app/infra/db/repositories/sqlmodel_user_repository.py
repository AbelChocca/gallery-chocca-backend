from app.infra.db.repositories.base_repository import BaseRepository
from app.domain.user.entity import User
from app.domain.user.user_exception import UserNotFoundException
from app.infra.db.models.model_user import UserTable

from sqlmodel import select

class PostgresUserRepository(BaseRepository[User, UserTable]):
    async def get_by_email(self, email: str) -> User:
        statement = select(UserTable).where(UserTable.email == email)
        user_db = (await self._db_session.exec(statement)).first()
        if not user_db:
            raise UserNotFoundException(f"User with email={email} not found")
        return self._base_mapper.to_entity(user_db)