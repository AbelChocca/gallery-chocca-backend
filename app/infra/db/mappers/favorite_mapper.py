from app.infra.db.mappers.base_mapper import BaseMapper
from app.infra.db.models.model_favorites import FavoritesTable
from app.domain.favorites.favorite_entity import FavoriteEntity

from typing import Optional

class FavoritesMapper(BaseMapper[FavoriteEntity, FavoritesTable]):
    @staticmethod
    def to_entity(model: FavoritesTable) -> FavoriteEntity:
        return FavoriteEntity(
            user_id=model.user_id,
            session_id=model.session_id,
            product_id=model.product_id,
            created_at=model.created_at,
            id=model.id
        )
    
    @staticmethod
    def to_db_model(entity: FavoriteEntity, existing_model: Optional[FavoritesTable] = None):
        if existing_model:
            existing_model.user_id = entity.user_id
            existing_model.session_id = entity.session_id
            return existing_model
        return FavoritesTable(
            session_id=entity.session_id,
            user_id=entity.user_id,
            product_id=entity.product_id,
            created_at=entity.created_at
        )