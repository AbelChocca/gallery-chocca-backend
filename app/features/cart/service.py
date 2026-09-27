from app.features.cart.cart_repository import CartRepository
from app.infra.db.repositories.product_repository import PostgresProductRepository
from app.features.inventory.repositories.inventory_repository import InventoryRepository
from app.core.exceptions import ValidationError
from app.features.cart.entities.cart import Cart
from app.features.cart.types import CartItemRow
from app.features.inventory.types.inventory_movement import InventoryOwnerType


class CartService:
    def __init__(
            self,
            cart_repository: CartRepository,
            product_repository: PostgresProductRepository,
            inventory_repository: InventoryRepository
        ):
        self._cart_repository = cart_repository
        self._product_repository = product_repository
        self._inventory_repo = inventory_repository

    async def add_item(
        self,
        product_id: int,
        variant_id: int,
        variant_size_id: int,
        quantity: int = 1,
        user_id: int | None = None,
        session_id: str | None = None,
    ) -> None:

        await self._validate_product_stock(
            product_id=product_id,
            variant_size_id=variant_size_id,
            quantity=quantity
        )

        cart = await self._get_or_create_active_cart(
            user_id=user_id,
            session_id=session_id
        )

        await self._cart_repository.add_item(
            cart.id,
            product_id,
            variant_id,
            variant_size_id,
            quantity
        )

    async def delete_product_from_carts(
        self,
        product_id: int,
    ) -> None:
        await self._cart_repository.delete_product_from_carts(
            product_id
        )
    
    async def clear_cart(
        self,
        cart_id: int
    ) -> None:

        await self._cart_repository.clear_cart(
            cart_id
        )
    
    async def set_item_quantity(
        self,
        cart_item_id: int,
        quantity: int,
    ) -> None:

        if quantity <= 0:
            raise ValidationError(
                "Quantity must be greater than 0",
                {
                    "event": "set_item_quantity",
                    "cart_item_id": cart_item_id,
                    "quantity": quantity,
                }
            )

        item = await self._cart_repository.get_cart_item_by_id(
            cart_item_id,
            raises=True
        )

        await self._validate_product_stock(
            product_id=item.product_id,
            variant_size_id=item.variant_size_id,
            quantity=quantity
        )

        item.quantity = quantity

        await self._cart_repository.update_item(item)
    
    async def increment_item_quantity(
        self,
        cart_item_id: int,
    ) -> None:
        item = await self._cart_repository.get_cart_item_by_id(cart_item_id, raises=True)

        new_quantity = item.quantity + 1

        await self._validate_product_stock(
            product_id=item.product_id,
            variant_size_id=item.variant_size_id,
            quantity=new_quantity
        )

        item.quantity = new_quantity

        await self._cart_repository.update_item(item)
    
    async def decrement_item_quantity(
        self,
        cart_item_id: int,
    ):
        item = await self._cart_repository.get_cart_item_by_id(cart_item_id, True)

        if item.quantity <= 1:
            raise ValidationError(
                "Quantity cannot be less than 1"
            )

        item.quantity -= 1

        await self._cart_repository.update_item(item)

    async def remove_item_from_cart(
        self,
        cart_item_id: int
    ) -> None:
        await self._cart_repository.delete_item(cart_item_id)
    
    async def get_cart_by_owner(
        self,
        *,
        user_id: int | None,
        session_id: str | None,
    ) -> Cart | None:
        return await self._cart_repository.get_active_cart(
            user_id=user_id,
            session_id=session_id,
        )

    async def get_cart_items(
        self,
        *,
        cart_id: int,
    ) -> list[CartItemRow]:
        return await self._cart_repository.get_cart_items_detail(
            cart_id=cart_id,
        )
    
    async def merge_guest_cart_to_user_cart(
        self,
        session_id: str,
        user_id: int,
    ) -> None:
        guest_cart = await self._cart_repository.get_active_cart_by_session_id(
            session_id=session_id,
            raises=False
        )

        # no guest cart → nothing to merge
        if not guest_cart:
            return

        user_cart = await self._cart_repository.get_active_cart_by_user_id(
            user_id=user_id,
            raises=False
        )

        # user still has no cart
        # easiest + fastest path:
        # migrate ownership
        if not user_cart:

            await self._cart_repository.migrate_session_cart_to_user(
                session_id=session_id,
                user_id=user_id
            )

            return

        # merge items into existing user cart
        for guest_item in guest_cart.items:
            existing_item = user_cart.find_item(
                product_id=guest_item.product_id,
                variant_id=guest_item.variant_id,
                variant_size_id=guest_item.variant_size_id
            )

            merged_quantity = guest_item.quantity

            if existing_item:
                merged_quantity += existing_item.quantity

            variant_size = await self._product_repository.get_variant_size_by_id(
                guest_item.variant_size_id,
                with_lock=True
            )

            # clamp quantity to available stock
            final_quantity = min(
                merged_quantity,
                variant_size.stock
            )

            # item already exists in user cart
            if existing_item:

                existing_item.quantity = final_quantity

                await self._cart_repository.update_item(
                    existing_item
                )

            # new item
            else:

                user_cart.add_item(
                    product_id=guest_item.product_id,
                    variant_id=guest_item.variant_id,
                    variant_size_id=guest_item.variant_size_id,
                    quantity=final_quantity
                )

        # persist new inserted items
        await self._cart_repository.save(user_cart)

        # remove guest cart after merge
        await self._cart_repository.delete_cart(
            guest_cart.id
        )
    
    async def _validate_product_stock(
        self,
        product_id: int,
        variant_size_id: int,
        quantity: int
    ) -> None:
        product = await self._product_repository.get_by_id(product_id)

        if not product.is_active:
            raise ValidationError(
                f"Product {product.nombre} is inactive"
            )

        available_total_stock = await self._inventory_repo.get_available_total_stock_by_owner(
            owner_type=InventoryOwnerType.PRODUCT,
            owner_id=variant_size_id
        )

        if available_total_stock < quantity:
            raise ValidationError(
                f"Insufficient stock. Available: {available_total_stock}"
            )
    
    async def _get_or_create_active_cart(
        self,
        user_id: int | None = None,
        session_id: str | None = None,
    ) -> Cart:

        if user_id is not None:

            cart = await self._cart_repository.get_active_cart_by_user_id(
                user_id=user_id,
                raises=False
            )

            if cart:
                return cart

            cart = Cart(
                user_id=user_id
            )

            return await self._cart_repository.save(
                cart
            )

        cart = await self._cart_repository.get_active_cart_by_session_id(
            session_id=session_id,
            raises=False
        )

        if cart:
            return cart

        cart = Cart(
            session_id=session_id
        )

        return await self._cart_repository.save(
            cart
        )