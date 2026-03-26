from app.infra.db.repositories.base_repository import BaseRepository
from app.domain.user.entity import User
from app.infra.db.models.model_user import UserTable
from app.core.exceptions import ValueNotFound

from sqlmodel import select, col, func
from typing import List

class PostgresUserRepository(BaseRepository[User, UserTable]):
    async def get_by_email(self, email: str) -> User:
        statement = select(UserTable).where(UserTable.email == email)
        user_db = (await self._db_session.execute(statement)).scalar()
        if not user_db:
            raise ValueNotFound(
                "User not found", 
                {
                    "repository": "postgres_user",
                    "event": "get_by_email"
                }
            )
        return self._base_mapper.to_entity(user_db)
    
    async def count_all(
            self, 
            related_name: str | None = None,
    ) -> int:
        stmt = (
            select(func.count(UserTable.id))
            .where(col(UserTable.nombre).ilike(f"%{related_name}%"))
        )

        count = (await self._db_session.execute(stmt)).scalar()
        return count
    
    async def get_all(
            self, 
            *,
            related_name: str | None = None,
            offset: int = 0,
            limit: int = 20
            ) -> List[User]:
        statement = select(UserTable)
        if related_name:
            statement = statement.where(col(UserTable.nombre).ilike(f"%{related_name}%"))
        statement = (
            statement
            .order_by(
                col(UserTable.created_at).desc(),
                col(UserTable.id).desc()
                )
            .offset(offset)
            .limit(limit)
        )

        users = (await self._db_session.execute(statement)).scalars().all()

        return [
            self._base_mapper.to_entity(user)
            for user in users
        ]