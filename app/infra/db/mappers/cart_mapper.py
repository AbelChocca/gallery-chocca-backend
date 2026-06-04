from app.features.cart.entities.cart import Cart
from app.features.cart.entities.cart_item import CartItem

from app.infra.db.models.model_cart import CartTable, CartItemTable
from app.infra.db.mappers.base_mapper import BaseMapper

class CartMapper(BaseMapper[Cart, CartTable]):

    @staticmethod
    def to_db_model(entity: Cart, existing_model: CartTable | None = None) -> CartTable:
        if existing_model:
            existing_model.user_id = entity.user_id
            existing_model.session_id = entity.session_id
            existing_model.status = entity.status
            existing_model.created_at = entity.created_at
            existing_model.updated_at = entity.updated_at
            existing_model.expires_at = entity.expires_at

            return existing_model
        
        return CartTable(
            user_id=entity.user_id,
            session_id=entity.session_id,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            expires_at=entity.expires_at
        )
    
    @staticmethod
    def to_entity(model: CartTable) -> Cart:

        cart = Cart(
            id=model.id,
            user_id=model.user_id,
            session_id=model.session_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            expires_at=model.expires_at,
            items=[]
        )

        for item in model.items:
            cart.items.append(
                CartItem(
                    id=item.id,
                    cart_id=item.cart_id,
                    product_id=item.product_id,
                    variant_id=item.variant_id,
                    variant_size_id=item.variant_size_id,
                    quantity=item.quantity,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                )
            )

        return cart
