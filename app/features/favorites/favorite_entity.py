from datetime import datetime, timezone

class FavoriteEntity:
    def __init__(
            self,
            product_id: int,
            created_at: datetime | None = None,
            user_id: int | None = None,
            session_id: str | None = None,
            id: int | None = None
            ):
        self.user_id: int | None = user_id
        self.session_id: str | None = session_id
        self.product_id: int = product_id
        self.created_at: datetime = created_at or datetime.now(timezone.utc)
        self.id: int | None = id