from app.domain.favorites.favorite_entity import FavoriteEntity
from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_favorites import FavoritesTable
from app.infra.db.exceptions import DatabaseException, ModelNotFound

from typing import List, Optional
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError

class PostgresFavoritesRepository(BaseRepository[FavoriteEntity, FavoritesTable]):
    async def _get_favorite_by_session_id(
            self, 
            product_id: int,
            session_id: int
        ) -> FavoritesTable:
        statement = (
            select(FavoritesTable)
            .where(FavoritesTable.product_id == product_id)
            .where(FavoritesTable.session_id == session_id)
        )
        result = (await self._db_session.exec(statement)).first()
        if not result:
            raise ModelNotFound(f"Favorite Model with product id: {product_id} and session id: {session_id} wasn't found")
        return result

    async def _get_favorite_by_user_id(
            self, 
            product_id: int,
            user_id: int
        ) -> FavoritesTable:
        statement = (
            select(FavoritesTable)
            .where(FavoritesTable.product_id == product_id)
            .where(FavoritesTable.user_id == user_id)
        )

        result = (await self._db_session.exec(statement)).first()
        if not result:
            raise ModelNotFound(f"Favorite Model with product id: {product_id} and user id: {user_id} wasn't found")
        return result

    async def delete_favorite_by_user_id(
            self, 
            product_id: int,
            user_id: int
            ) -> None:
        try:
            favorite_model = await self._get_favorite_by_user_id(product_id, user_id)

            await self._db_session.delete(favorite_model)
            await self._db_session.commit()
        except SQLAlchemyError as s:
            await self._db_session.rollback()
            raise DatabaseException(f"Failed to delete the favorite by user with id: {user_id}, traceback: {str(s)}")

    async def delete_favorite_by_session_id(
            self, 
            product_id: int,
            session_id: int
            ) -> None:
        try:
            favorite_model = await self._get_favorite_by_session_id(product_id, session_id)

            await self._db_session.delete(favorite_model)
            await self._db_session.commit()
        except SQLAlchemyError as s:
            await self._db_session.rollback()
            raise DatabaseException(f"Failed to delete the favorite by session with id: {session_id}, traceback: {str(s)}")

    async def get_favorite_status(
        self,
        *,
        product_id: int,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> bool:
        statement = (
            select(FavoritesTable)
            .where(FavoritesTable.product_id == product_id)
        )
        if user_id:
            statement = statement.where(FavoritesTable.user_id == user_id)
        else:
            statement = statement.where(FavoritesTable.session_id == session_id)

        result = (await self._db_session.exec(statement)).first()
        if not result:
            return False
        return True

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