from app.api.schemas.favorites.schema import FavoritesFilterSchema
from app.domain.favorites.dto import FavoritesFilter

class FavoriteSchemaToMapper:
    @staticmethod
    def filter_schema_to_dto(schema: FavoritesFilterSchema) -> FavoritesFilter:
        return FavoritesFilter(
            related_search=schema.related_search,
            order_by=schema.order_by
        )
