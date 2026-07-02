from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Enum, func, UniqueConstraint, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped

from app.features.cart.types import CartStatus

class CartTable(SQLModel, table=True):
    __tablename__ = "carts"
    __table_args__ = (
        CheckConstraint(
            (
                "(user_id IS NOT NULL AND session_id IS NULL)"
                " OR "
                "(user_id IS NULL AND session_id IS NOT NULL)"
            ),
            name="ck_cart_user_or_session"
        ),

        UniqueConstraint(
            "user_id",
            name="uq_cart_user"
        ),

        UniqueConstraint(
            "session_id",
            name="uq_cart_session"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(
        default=None,
        index=True,
        description="ID del usuario autenticado (nullable para guest)"
    )

    session_id: str | None = Field(
        default=None,
        index=True,
        description="ID de sesión para usuarios guest"
    )

    status: CartStatus = Field(
        default=CartStatus.ACTIVE,
        sa_column=Column(Enum(CartStatus, name="cart_status_type"), index=True, nullable=False)
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(True)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(True), default=func.now(), onupdate=func.now()))

    expires_at: datetime | None = Field(default=None)

    items: Mapped[list['CartItemTable']] = Relationship(back_populates="cart", sa_relationship_kwargs={
        "cascade": "all, delete-orphan",
        "lazy": "selectin"
    })

class CartItemTable(SQLModel, table=True):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            "variant_id",
            "variant_size_id",
            name="uq_cart_item_unique_line"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    cart_id: int = Field(
        sa_column=Column(
            ForeignKey("carts.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )

    product_id: int = Field(index=True)
    variant_id: int = Field(index=True)
    variant_size_id: int = Field(index=True)

    quantity: int = Field(default=1)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(True)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(True), default=func.now(), onupdate=func.now()))

    cart: Mapped['CartTable'] = Relationship(back_populates="items")