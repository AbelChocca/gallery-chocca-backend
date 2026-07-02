from app.infra.db.repositories.sqlalchemy_cart_repository import CartRepository
from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.core.exceptions import ValueNotFound, ValidationError
from app.features.cart.entities.cart import Cart
from app.features.cart.types import CartItemRow
from app.features.pricing.utils.pricing_calculator import ProductPricingCalculator
from app.infra.db.repositories.sqlalchemy_product_pricing_rule_repository import ProductPricingRepository

from collections import defaultdict

class CartService:
    def __init__(
            self,
            cart_repository: CartRepository,
            product_repository: PostgresProductRepository,
            product_pricing_repository: ProductPricingRepository,
            pricing_calculator: ProductPricingCalculator
        ):
        self._cart_repository = cart_repository
        self._product_repository = product_repository
        self._pricing_calculator = pricing_calculator
        self._product_pricing_repository = product_pricing_repository

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
    
    async def get_full_cart_by_owner(
            self, 
            user_id: int | None,
            session_id: str | None,
            ) -> dict | None:
        cart = await self._cart_repository.get_active_cart(
            user_id=user_id,
            session_id=session_id,
        )

        if not cart:
            return None
        
        cart_items = await self._cart_repository.get_full_cart(cart.id)

        if not cart_items:
            return {
                "cart_id": cart.id,
                "items": [],
                "subtotal": 0,
                "total": 0,
                "total_items": 0,
            }
        
        product_ids: list[int] = [item["product_id"] for item in cart_items]
        
        rules = await (
            self._product_pricing_repository
            .get_product_pricing_rules_summary(
                product_ids=product_ids
            )
        )

        rules_by_product = defaultdict(list)

        for rule in rules:
            rules_by_product[rule.product_id].append(rule)
        
        parsed_items = []

        subtotal = 0
        total = 0
        
        for item in cart_items:
            item: CartItemRow = dict(item)

            product_rules = rules_by_product.get(
                item["product_id"],
                []
            )

            pricing_result = self._pricing_calculator.calculate(
                base_price=item['base_price'],
                rules=product_rules
            )

            item["final_price"] = pricing_result.final_price

            item["available_quantity"] = min(
                item["stock"],
                item["quantity"]
            )

            item["is_available"] = (
                item["has_stock"] and
                item["is_product_active"]
            )

            item["subtotal"] = (
                item["quantity"] *
                item["base_price"]
            )

            item["final_subtotal"] = (
                item["quantity"] *
                pricing_result.final_price
            )

            subtotal += item["subtotal"]
            total += item["final_subtotal"]

            parsed_items.append(item)

        return {
            "cart_id": cart.id,
            "items": parsed_items,
            "subtotal": subtotal,
            "total": total,
            "total_items": len(parsed_items)
        }
    
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
    
    async def _get_cart_or_raise(self, cart_id: int) -> Cart:
        cart = await self._cart_repository.get_by_id_with_items(cart_id)

        if not cart:
            raise ValueNotFound(
                "Cart not found",
                {
                    "cart_id": cart_id
                }
            )

        return cart
    
    async def _validate_product_stock(
        self,
        product_id: int,
        variant_size_id: int,
        quantity: int
    ):
        product = await self._product_repository.get_by_id(product_id)

        if not product.is_active:
            raise ValidationError(
                f"Product {product.nombre} is inactive"
            )

        variant_size = await self._product_repository.get_variant_size_by_id(
            variant_size_id,
            with_lock=True
        )

        if variant_size.stock < quantity:
            raise ValidationError(
                f"Insufficient stock. Available: {variant_size.stock}"
            )

        return variant_size
    
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