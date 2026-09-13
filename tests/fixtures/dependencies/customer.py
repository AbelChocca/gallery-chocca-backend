import pytest_asyncio

from app.features.sales.models.customer import Customer
from app.features.sales.types.customer import CustomerType


@pytest_asyncio.fixture
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