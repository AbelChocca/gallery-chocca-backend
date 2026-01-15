from app.domain.favorites.favorite_entity import FavoriteEntity
from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_favorites import FavoritesTable
from app.infra.db.exceptions import DatabaseException

from typing import List
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError

class PostgresFavoritesRepository(BaseRepository[FavoriteEntity, FavoritesTable]):

    async def get_favorites_by_user_id(self, user_id: int) -> List[int]:
        try:
            statement = (
                select(FavoritesTable.product_id).
                where(FavoritesTable.user_id == user_id)
                .order_by(FavoritesTable.created_at)
            )
            response: List[int] = (await self._db_session.exec(statement)).all()

            return response
        except SQLAlchemyError as s:
            raise DatabaseException(f"Error while getting the favorites of user with id: {user_id}, traceback: {str(s)}")
        
    async def get_favorites_by_session_id(self, session_id: int) -> List[int]:
        try:
            statement = (
                select(FavoritesTable.product_id).
                where(FavoritesTable.session_id == session_id)
                .order_by(FavoritesTable.created_at)
            )
            response: List[int] = (await self._db_session.exec(statement)).all()

            return response
        except SQLAlchemyError as s:
            raise DatabaseException(f"Error while getting the favorites of anonymous with id: {session_id}, traceback: {str(s)}")