from fastapi import Depends

from app.infra.db.uow.dependency import (
    get_uow,
)
from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)

from app.api.security.resolvers.sessions import (
    get_user_id,
)
from app.features.customer.dtos.customer import (
    CustomerPricingContext,
)


async def get_customer_pricing_context(
    user_id: int | None = Depends(get_user_id),
    uow: UnitOfWork = Depends(get_uow),
) -> CustomerPricingContext | None:

    if user_id is None:
        return None

    return await uow.customers.get_pricing_context_by_user_id(
        user_id=user_id
    )