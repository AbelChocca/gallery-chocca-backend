import pytest_asyncio

from app.features.customer.models.customer import Customer
from app.features.sales.types.customer import CustomerType


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def pricing_customer(db_session):
    customer = Customer(
        customer_type=CustomerType.REGULAR,
        name="Pricing Test Customer",
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
        email="wholesale-pricing@example.com",
        phone="988888888",
    )

    db_session.add(customer)

    await db_session.commit()
    await db_session.refresh(customer)

    return customer