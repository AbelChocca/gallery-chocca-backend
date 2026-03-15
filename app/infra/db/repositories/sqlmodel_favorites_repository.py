from app.domain.favorites.favorite_entity import FavoriteEntity
from app.domain.favorites.dto import FavoritesFilter
from app.domain.product.entities.product import Product
from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_favorites import FavoritesTable
from app.infra.db.models.model_product import ProductTable, VariantTable
from app.infra.db.exceptions import DatabaseException
from app.infra.db.mappers.product_mapper import ProductMapper
from app.shared.dtos import OrderByEnum

from typing import List
from sqlmodel import col
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, noload
from sqlalchemy import func, select, delete, update

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
        result = (await self._db_session.execute(statement)).scalar()
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

        result = (await self._db_session.execute(statement)).scalar()
        return result

    async def delete_favorite_by_user_id(
            self, 
            product_id: int,
            user_id: int
            ) -> None:
        try:
            stmt = (
                delete(FavoritesTable)
                .where(FavoritesTable.product_id == product_id)
                .where(FavoritesTable.user_id == user_id)
            )

            await self._db_session.execute(stmt)
        except SQLAlchemyError as s:
            raise DatabaseException(
                f"Failed to delete the favorite by user id",
                {
                    "repository": "postgres_favorite",
                    "user_id": user_id,
                    "event": "delete_favorite_by_user_id"
                }
                ) from s

    async def delete_favorite_by_session_id(
            self, 
            product_id: int,
            session_id: int
            ) -> None:
        try:
            stmt = (
                delete(FavoritesTable)
                .where(FavoritesTable.product_id == product_id)
                .where(FavoritesTable.session_id == session_id)
            )

            await self._db_session.execute(stmt)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Failed to delete the favorite by session id",
                {
                    "repository": "postgres_favorite",
                    "session_id": session_id,
                    "event": "delete_favorite_by_session_id"
                }
                ) from s

    async def get_favorite_status(
        self,
        *,
        product_id: int,
        user_id: int | None = None,
        session_id: str | None = None
    ) -> bool:
        if user_id:
            favorite_model = await self._get_favorite_by_user_id(product_id, user_id)
        else:
            favorite_model = await self._get_favorite_by_session_id(product_id, session_id)

        return favorite_model is not None

    async def get_favorites_by_user_id(
            self, 
            *,
            filter: FavoritesFilter,
            user_id: int,
            offset: int = 0,
            limit: int = 20,
            ) -> List[Product]:
        statement = (
            select(ProductTable)
            .options(
                selectinload(ProductTable.variants)
                .options(noload(VariantTable.sizes))
            )
            .select_from(FavoritesTable)
            .join(
            ProductTable,
            ProductTable.id == FavoritesTable.product_id
            )
            .where(FavoritesTable.user_id == user_id)
        )
        if filter.related_search:
            statement = statement.where(col(ProductTable.nombre).ilike(f"%{filter.related_search}%"))

        if filter.order_by == OrderByEnum.newest:
            order = col(FavoritesTable.created_at).desc()
        else:
            order = col(FavoritesTable.created_at).asc()

        statement = (
            statement
            .order_by(order)
            .offset(offset)
            .limit(limit)
        )
        response: List[ProductTable] = (await self._db_session.execute(statement)).scalars().all()

        return [
            ProductMapper.to_entity(product_table)
            for product_table in response
        ]
        
    async def get_favorites_by_session_id(
            self, 
            *,
            filter: FavoritesFilter,
            session_id: int,
            offset: int = 0,
            limit: int = 20,
        ) -> List[Product]:
        statement = (
            select(ProductTable)
            .options(
                selectinload(ProductTable.variants)
                .options(noload(VariantTable.sizes))
            )
            .select_from(FavoritesTable)
            .join(
            ProductTable,
            ProductTable.id == FavoritesTable.product_id
            )
            .where(FavoritesTable.session_id == session_id)
        )
        if filter.related_search:
            statement = statement.where(col(ProductTable.nombre).ilike(f"%{filter.related_search}%"))

        if filter.order_by == OrderByEnum.newest:
            order = col(FavoritesTable.created_at).asc()
        else:
            order = col(FavoritesTable.created_at).desc()

        statement = (
            statement
            .order_by(order)
            .offset(offset)
            .limit(limit)
        )
        response: List[ProductTable] = (await self._db_session.execute(statement)).scalars().all()

        return [
            ProductMapper.to_entity(product_table)
            for product_table in response
        ]
    
    async def count_favorites(self, *, user_id: int | None = None, session_id: int | None = None) -> int:
        statement = (
            select(func.count(FavoritesTable.id))
        )

        if user_id:
            statement = statement.where(FavoritesTable.user_id == user_id)
        else:
            statement = statement.where(FavoritesTable.session_id == session_id)

        result = (await self._db_session.execute(statement)).scalar()

        return result or 0
    
    async def delete_favorite_of_product(self, product_id: int) -> None:
        try:
            stmt = delete(FavoritesTable).where(FavoritesTable.product_id == product_id)

            await self._db_session.execute(stmt)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres delete failed",
                {
                    "product_id": product_id,
                    "event": "delete_favorite_of_product",
                    "repository": "postgres_favorite"
                }
                ) from s
        
    async def set_anon_session_favorites_to_user_favorites(
            self, 
            anon_session_id: int,
            new_user_id: int
    ) -> None:
        try:
            stmt = (
                update(FavoritesTable)
                .where(FavoritesTable.session_id == anon_session_id)
                .where(
                    ~col(FavoritesTable.user_id).in_(
                        select(FavoritesTable.product_id)
                        .where(FavoritesTable.user_id == new_user_id)
                    )
                )
                .values({"user_id": new_user_id, "session_id": None})
            )

            await self._db_session.execute(stmt)
        except SQLAlchemyError as s:
            raise DatabaseException(    
                "Postgres setting failed",
                {
                    "repository": "postgres_favorite",
                    "event": "set_anon_session_favorites_to_user_favorites",
                    "anon_session_id": anon_session_id,
                    "new_user_id": new_user_id
                }
            ) from s
