import pytest_asyncio

from app.infra.db.models.model_cart import (
    CartTable,
    CartItemTable,
)

from app.features.cart.types import CartStatus


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def wholesale_cart(
    db_session,
    admin_user,
    product,
    variant,
    variant_size,
    variant_size_inventory,
):
    user = admin_user["user"]

    cart = CartTable(
        user_id=user.id,
        session_id=None,
        status=CartStatus.ACTIVE,
    )

    db_session.add(cart)
    await db_session.flush()

    cart_item = CartItemTable(
        cart_id=cart.id,
        product_id=product.id,
        variant_id=variant.id,
        variant_size_id=variant_size.id,
        quantity=2,
    )

    db_session.add(cart_item)

    await db_session.commit()

    await db_session.refresh(cart)
    await db_session.refresh(cart_item)

    return {
        "cart": cart,
        "item": cart_item,
    }