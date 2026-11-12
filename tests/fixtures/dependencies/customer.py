import pytest_asyncio

from app.features.customer.models.customer import Customer
from app.features.customer.customer_types import CustomerType



@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def pricing_customer(
    db_session,
    admin_user,
):
    customer = Customer(
        user_id=admin_user["user"].id,
        session_id=None,
        customer_type=CustomerType.REGULAR,
        name="Pricing Test",
        last_name="Customer",
        email="pricing-test@example.com",
        phone="999999999",
    )

    db_session.add(customer)

    await db_session.commit()
    await db_session.refresh(customer)

    return customer


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def wholesale_pricing_customer(
    db_session,
    admin_user,
):
    admin = admin_user["user"]

    customer = Customer(
        user_id=admin.id,
        customer_type=CustomerType.WHOLESALE,
        name="Wholesale Pricing Customer",
        last_name="Customer",
        email="wholesale-pricing@example.com",
        phone="988888888",
    )

    db_session.add(customer)

    await db_session.commit()
    await db_session.refresh(customer)

    return customer