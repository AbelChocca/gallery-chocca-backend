from datetime import datetime, timezone
from app.features.cart.types import CartStatus

from app.features.cart.entities.cart_item import CartItem

class Cart:
    def __init__(
        self,
        id: int | None = None,
        user_id: int | None = None,
        session_id: str | None = None,
        status: CartStatus = CartStatus.ACTIVE,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        expires_at: datetime | None = None,
        items: list["CartItem"] | None = None,
    ):
        self.id = id
        self.user_id = user_id
        self.session_id = session_id
        self.status = status

        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        self.expires_at = expires_at

        self.items: list["CartItem"] = items or []

    def add_item(
        self,
        product_id: int,
        variant_id: int,
        variant_size_id: int,
        quantity: int = 1,
    ) -> CartItem:

        existing_item = next(
            (
                item for item in self.items
                if item.product_id == product_id
                and item.variant_id == variant_id
                and item.variant_size_id == variant_size_id
            ),
            None
        )

        if existing_item:
            existing_item.quantity += quantity
            self._touch()
            return existing_item

        new_item = CartItem(
            id=None,
            cart_id=self.id,
            product_id=product_id,
            variant_id=variant_id,
            variant_size_id=variant_size_id,
            quantity=quantity,
        )

        self.items.append(new_item)
        self._touch()

        return new_item
    
    def find_item(
        self,
        product_id: int,
        variant_id: int,
        variant_size_id: int,
    ) -> CartItem | None:

        return next(
            (
                item
                for item in self.items
                if (
                    item.product_id == product_id
                    and item.variant_id == variant_id
                    and item.variant_size_id == variant_size_id
                )
            ),
            None
        )

    def _touch(self):
        self.updated_at = datetime.now(timezone.utc)