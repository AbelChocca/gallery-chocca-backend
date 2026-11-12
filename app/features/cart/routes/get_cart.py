from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.features.cart.cart_route import router
from app.features.cart.dependencies.use_cases.get_full_cart import (
    get_full_cart_use_case,
)
from app.features.cart.schema import (
    GetFullCartResponse,
)
from app.features.cart.use_cases.get_full_cart import (
    GetFullCartUseCase,
)
from app.features.customer.helpers.get_customer_pricing_context import (
    get_customer_pricing_context,
)
from app.features.customer.dtos.customer import (
    CustomerPricingContext,
)

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)


@router.get(
    "",
    response_model=GetFullCartResponse | None,
    status_code=status.HTTP_200_OK,
    summary="Get current cart",
)
async def get_cart(
    use_case: Annotated[
        GetFullCartUseCase,
        Depends(get_full_cart_use_case),
    ],
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    customer: Annotated[
        CustomerPricingContext | None,
        Depends(get_customer_pricing_context),
    ],
) -> GetFullCartResponse | None:

    result = await use_case.execute(
        user_id=owner.user_id,
        session_id=owner.session_id,
        customer_id=(
            customer.customer_id
            if customer
            else None
        ),
        customer_type=(
            customer.customer_type
            if customer
            else None
        ),
    )

    if result is None:
        return None

    return GetFullCartResponse.model_validate(
        result
    )