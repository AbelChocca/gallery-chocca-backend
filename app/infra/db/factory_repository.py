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

from app.core.log.protocole import LoggerProtocol

from sqlmodel.ext.asyncio.session import AsyncSession

class FactoryRespository:
    def __init__(
            self,
            db_session: AsyncSession,
            logger: LoggerProtocol
            ):
        self._db_session: AsyncSession = db_session
        self._logger: LoggerProtocol = logger

    def get_product_repository(self) -> PostgresProductRepository:
        return PostgresProductRepository(
            db_session=self._db_session,
            base_mapper=ProductMapper,
            logger=self._logger,
            base_model=ProductTable
        )
    
    def get_slide_repository(self) -> PostgresSlideRepository:
        return PostgresSlideRepository(
            db_session=self._db_session,
            base_mapper=SlideMapper,
            logger=self._logger,
            base_model=SlideTable
        )
    
    def get_image_repository(self) -> PostgresImageRepository:
        return PostgresImageRepository(
            db_session=self._db_session,
            base_mapper=ImageMapper,
            logger=self._logger,
            base_model=MediaImageTable
        )
    
    def get_user_repository(self) -> PostgresUserRepository:
        return PostgresUserRepository(
            db_session=self._db_session,
            base_mapper=UserMapper,
            logger=self._logger,
            base_model=UserTable
        )
    
    def get_favorite_repository(self) -> PostgresFavoritesRepository:
        return PostgresFavoritesRepository(
            db_session=self._db_session,
            base_mapper=FavoritesMapper,
            logger=self._logger,
            base_model=FavoritesTable
        )