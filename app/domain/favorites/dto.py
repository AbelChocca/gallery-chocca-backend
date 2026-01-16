from dataclasses import dataclass

@dataclass(frozen=True)
class FavoriteStatus:
    is_favorite: bool