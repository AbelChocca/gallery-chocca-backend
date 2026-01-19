from datetime import datetime, timezone
from typing import Optional

class FavoriteEntity:
    def __init__(
            self,
            product_id: int,
            created_at: Optional[datetime] = None,
            user_id: Optional[int] = None,
            session_id: Optional[str] = None,
            id: Optional[int] = None
            ):
        self.user_id: Optional[int] = user_id
        self.session_id: Optional[str] = session_id
        self.product_id: int = product_id
        self.created_at: datetime = created_at or datetime.now(timezone.utc)
        self.id: Optional[int] = id