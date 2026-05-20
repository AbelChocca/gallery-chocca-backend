from pydantic import BaseModel, ConfigDict, Field

from app.shared.dtos import OrderByEnum

class FavoriteStatusSchema(BaseModel):
    is_favorite: bool

    model_config = ConfigDict(from_attributes=True)

class CountFavoritesSchema(BaseModel):
    total_favorites: int

    model_config = ConfigDict(from_attributes=True)

class FavoritesFilterSchema(BaseModel):
    related_search: str | None = Field(default=None, examples=[None])
    order_by: OrderByEnum = OrderByEnum.newest
