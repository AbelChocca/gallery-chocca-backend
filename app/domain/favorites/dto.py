from dataclasses import dataclass

from app.shared.dtos import OrderByEnum

@dataclass(frozen=True)
class FavoritesFilter:
    related_search: str | None = None
    order_by: OrderByEnum = OrderByEnum.newest