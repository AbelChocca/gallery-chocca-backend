from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import AbstractAsyncContextManager
from typing import Callable, Type

from app.infra.db.repositories.sqlalchemy_inventory_movement_repo import PostgresInventoryMovementReposity
from app.infra.db.mappers.inventory_movement_mapper import InventoryMovementMapper
from app.infra.db.models.model_inventory_movement import InventoryMovementTable

from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.mappers.product_mapper import ProductMapper
from app.infra.db.models.model_product import ProductTable

from app.infra.db.repositories.sqlmodel_slide_repository import PostgresSlideRepository
from app.infra.db.mappers.slide_mapper import SlideMapper
from app.infra.db.models.model_slide import SlideTable

from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.db.mappers.image_mapper import ImageMapper
from app.infra.db.models.model_media import MediaImageTable

from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.infra.db.mappers.user_mapper import UserMapper
from app.infra.db.models.model_user import UserTable

from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.infra.db.mappers.favorite_mapper import FavoritesMapper
from app.infra.db.models.model_favorites import FavoritesTable

class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self._session_factory()

        self.products = PostgresProductRepository(
            self.session,
            ProductMapper,
            ProductTable
        )
        self.slides = PostgresSlideRepository(
            self.session,
            SlideMapper,
            SlideTable
        )
        self.users = PostgresUserRepository(
            self.session,
            UserMapper,
            UserTable
        )
        self.favorites = PostgresFavoritesRepository(
            self.session,
            FavoritesMapper,
            FavoritesTable
        )
        self.images = PostgresImageRepository(
            self.session,
            ImageMapper,
            MediaImageTable
        )
        self.inventory = PostgresInventoryMovementReposity(
            self.session,
            InventoryMovementMapper,
            InventoryMovementTable
        )

        return self

    async def __aexit__(self, exc_type: Type[BaseException], exc, tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
