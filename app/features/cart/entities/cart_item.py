from datetime import datetime, timezone


class CartItem:
    def __init__(
        self,
        id: int | None = None,
        cart_id: int | None = None,
        product_id: int = None,
        variant_id: int = None,
        variant_size_id: int = None,
        quantity: int = 1,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.cart_id = cart_id

        self.product_id = product_id
        self.variant_id = variant_id
        self.variant_size_id = variant_size_id

        self.quantity = quantity

        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)