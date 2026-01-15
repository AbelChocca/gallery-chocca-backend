from datetime import datetime
from typing import Optional

class FavoriteEntity:
    def __init__(
            self,
            user_id: int,
            product_id: int,
            created_at: datetime,
            id: Optional[int] = None
            ):
        self.user_id: int = user_id
        self.product_id: int = product_id
        self.created_at: datetime = created_at
        self.id: Optional[int] = id