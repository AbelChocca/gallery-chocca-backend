from app.infra.db.repositories.base_repository import BaseRepository
from app.features.cart.entities.cart import Cart, CartItem
from app.infra.db.models.model_cart import CartTable, CartItemTable
from app.infra.db.models.model_product import ProductTable, VariantSizeTable, VariantTable
from app.infra.db.models.model_media import MediaImageTable
from app.features.cart.types import CartItemRow, CartStatus
from app.core.exceptions import ValueNotFound
from app.infra.db.exceptions import DatabaseException
from sqlalchemy import select, delete, or_, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlmodel import col

class CartRepository(BaseRepository[Cart, CartTable]):   
    async def update_item(
        self,
        item: CartItem
    ) -> None:
        try:
            existing_item = await self._get_cart_item_model_by_id(
                item.id,
                raises=True
            )

            existing_item.quantity = item.quantity
            existing_item.updated_at = item.updated_at

            self._db_session.add(existing_item)

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while updating cart item",
                {
                    "repository": "postgres_cart",
                    "event": "update_item",
                    "cart_item_id": item.id,
                    "original_error": str(
                        getattr(s, "orig", s)
                    )
                }
            ) from s
        
    async def add_item(
        self,
        cart_id: int,
        product_id: int,
        variant_id: int,
        variant_size_id: int,
        quantity: int,
    ):
        stmt = (
            insert(CartItemTable).values(
                cart_id=cart_id,
                product_id=product_id,
                variant_id=variant_id,
                variant_size_id=variant_size_id,
                quantity=quantity
            )
        )

        await self._db_session.execute(stmt)
        
    async def get_active_cart_by_user_id(
        self,
        user_id: int,
        raises: bool = True
    ) -> Cart | None:

        stmt = (
            select(CartTable)
            .options(
                selectinload(CartTable.items)
            )
            .where(
                CartTable.user_id == user_id,
                CartTable.status == CartStatus.ACTIVE
            )
        )

        result = await self._db_session.execute(stmt)

        cart_model = result.scalar_one_or_none()

        if not cart_model:
            if not raises:
                return None

            raise ValueNotFound(
                "Active cart wasn't found",
                {
                    "event": "get_active_cart_by_user_id",
                    "user_id": user_id,
                    "repository": "postgres_cart"
                }
            )

        return self._base_mapper.to_entity(cart_model)
    
    async def get_active_cart_by_session_id(
        self,
        session_id: str,
        raises: bool = True
    ) -> Cart | None:

        stmt = (
            select(CartTable)
            .options(
                selectinload(CartTable.items)
            )
            .where(
                CartTable.session_id == session_id,
                CartTable.status == CartStatus.ACTIVE
            )
        )

        result = await self._db_session.execute(stmt)

        cart_model = result.scalar_one_or_none()

        if not cart_model:
            if not raises:
                return None

            raise ValueNotFound(
                "Active cart wasn't found",
                {
                    "event": "get_active_cart_by_session_id",
                    "session_id": session_id,
                    "repository": "postgres_cart"
                }
            )

        return self._base_mapper.to_entity(cart_model)
    
    async def delete_cart(
        self,
        cart_id: int
    ) -> None:
        try:
            cart_model = await self._get_model_by_id_non_raise(
                cart_id
            )

            if not cart_model:
                raise ValueNotFound(
                    "Cart wasn't found",
                    {
                        "event": "delete_cart",
                        "cart_id": cart_id,
                        "repository": "postgres_cart"
                    }
                )

            await self._db_session.delete(cart_model)

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while deleting cart",
                {
                    "repository": "postgres_cart",
                    "event": "delete_cart",
                    "cart_id": cart_id,
                    "original_error": str(
                        getattr(s, "orig", s)
                    )
                }
            ) from s
        
    async def migrate_session_cart_to_user(
        self,
        session_id: str,
        user_id: int
    ) -> None:

        stmt = (
            select(CartTable)
            .where(
                CartTable.session_id == session_id,
                CartTable.status == CartStatus.ACTIVE
            )
        )

        result = await self._db_session.execute(stmt)

        cart = result.scalar_one_or_none()

        if not cart:
            return

        cart.user_id = user_id
        cart.session_id = None

        self._db_session.add(cart)
        
    async def delete_item(
        self,
        cart_item_id: int
    ) -> None:
        try:
            item_model = await self._get_cart_item_model_by_id(
                cart_item_id,
                raises=True
            )

            await self._db_session.delete(item_model)

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while deleting cart item",
                {
                    "repository": "postgres_cart",
                    "event": "delete_item",
                    "cart_item_id": cart_item_id,
                    "original_error": str(
                        getattr(s, "orig", s)
                    )
                }
            ) from s
        
    async def clear_cart(
        self,
        cart_id: int
    ) -> None:
        try:
            stmt = (
                delete(CartItemTable)
                .where(CartItemTable.cart_id == cart_id)
            )

            await self._db_session.execute(stmt)

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while clearing cart",
                {
                    "repository": "postgres_cart",
                    "event": "clear_cart",
                    "cart_id": cart_id,
                    "original_error": str(
                        getattr(s, "orig", s)
                    )
                }
            ) from s
        
    async def get_by_id_with_items(
        self,
        cart_id: int,
        raises: bool = True
    ) -> Cart | None:

        stmt = (
            select(CartTable)
            .options(
                selectinload(CartTable.items)
            )
            .where(CartTable.id == cart_id)
        )

        result = await self._db_session.execute(stmt)

        cart_model = result.scalar_one_or_none()

        if not cart_model:
            if not raises:
                return None

            raise ValueNotFound(
                "Cart wasn't found",
                {
                    "event": "get_by_id_with_items",
                    "cart_id": cart_id,
                    "repository": "postgres_cart"
                }
            )

        return self._base_mapper.to_entity(cart_model)
    
    async def get_cart_item_by_id(
        self,
        cart_item_id: int,
        raises: bool = True
    ) -> CartItem | None:
        stmt = (
            select(CartItemTable)
            .where(CartItemTable.id == cart_item_id)
        )

        result = await self._db_session.execute(stmt)

        cart_item_model = result.scalar_one_or_none()

        if not cart_item_model:
            if not raises:
                return None

            raise ValueNotFound(
                "Cart item wasn't found",
                {
                    "event": "get_cart_item_by_id",
                    "cart_item_id": cart_item_id,
                    "repository": "postgres_cart"
                }
            )

        return CartItem(
            id=cart_item_model.id,
            cart_id=cart_item_model.cart_id,
            product_id=cart_item_model.product_id,
            variant_id=cart_item_model.variant_id,
            variant_size_id=cart_item_model.variant_size_id,
            quantity=cart_item_model.quantity,
            created_at=cart_item_model.created_at,
            updated_at=cart_item_model.updated_at,
        )
     
    async def get_full_cart(self, cart_id: int) -> list[CartItemRow]:
        image_subq = (
            select(MediaImageTable.image_url)
            .where(
                MediaImageTable.owner_id == VariantTable.id,
                MediaImageTable.owner_type == "variant",
                col(MediaImageTable.is_primary).is_(True)
            )
            .limit(1)
            .scalar_subquery()
        )
        
        stmt = (
            select(
                col(CartItemTable.id).label("cart_item_id"),
                CartItemTable.quantity,

                col(ProductTable.id).label("product_id"),
                ProductTable.nombre,
                ProductTable.base_price,
                col(ProductTable.is_active).label("is_product_active"),
                col(VariantTable.id).label("variant_id"),
                VariantTable.color,

                col(VariantSizeTable.id).label("variant_size_id"),
                VariantSizeTable.size,
                VariantSizeTable.stock,
                VariantSizeTable.sku,
                (
                    VariantSizeTable.stock >= CartItemTable.quantity
                ).label("has_stock"),

                image_subq.label("image_url"),
            )
            .join(ProductTable, ProductTable.id == CartItemTable.product_id)
            .join(VariantTable, VariantTable.id == CartItemTable.variant_id)
            .join(VariantSizeTable, VariantSizeTable.id == CartItemTable.variant_size_id)
            .where(CartItemTable.cart_id == cart_id)
        )

        res = await self._db_session.execute(stmt)

        rows: list[CartItemRow] = res.mappings().all()

        return rows
    
    async def get_active_cart(
        self,
        user_id: int | None,
        session_id: str | None,
    ):
        stmt = select(CartTable).where(
            CartTable.status == CartStatus.ACTIVE,
            or_(
                CartTable.user_id == user_id,
                CartTable.session_id == session_id
            )
        )

        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def delete_items_by_variant_id(
        self,
        variant_ids: list[id]
    ) -> None:

        stmt = (
            delete(CartItemTable)
            .where(
                col(CartItemTable.variant_id).in_(variant_ids)
            )
        )

        await self._db_session.execute(stmt)

    async def delete_items_by_variant_size_ids(
        self,
        variant_size_ids: list[int]
    ) -> None:
        stmt = (
            delete(CartItemTable)
            .where(
                col(CartItemTable.variant_size_id).in_(variant_size_ids)
            )
        )

        await self._db_session.execute(stmt)
    
    async def _get_cart_item_model_by_id(
        self,
        cart_item_id: int,
        raises: bool = False
    ) -> CartItemTable | None:

        stmt = (
            select(CartItemTable)
            .where(CartItemTable.id == cart_item_id)
        )

        result = await self._db_session.execute(stmt)

        model = result.scalar_one_or_none()

        if not model and raises:
            raise ValueNotFound(
                "Cart item wasn't found",
                {
                    "event": "_get_cart_item_model_by_id",
                    "cart_item_id": cart_item_id,
                    "repository": "postgres_cart"
                }
            )

        return model
