from sqlmodel import SQLModel, Field, UniqueConstraint, CheckConstraint
from datetime import datetime, timezone
from typing import Optional


class FavoritesTable(SQLModel, table=True):
    __tablename__ = "favorites"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    session_id: Optional[int] = Field(default=None, index=True)
    user_id: Optional[int] = Field(default=None, index=True)

    product_id: int = Field(nullable=False, index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    __table__args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND session_id IS NULL "
            "OR (user_id IS NULL AND session_id IS NOT NULL)",
            name="ck_favorites_user_or_session"
            ),

        UniqueConstraint("user_id", "product_id", name="uq_favorites_user_product"),

        UniqueConstraint("session_id", "product_id", name="uq_favorites_session_product")
    )


