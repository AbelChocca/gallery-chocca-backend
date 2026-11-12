from typing import Annotated

from fastapi import Depends, status

from app.features.customer.customer_route import router
from app.features.customer.customer_service import (
    CustomerService,
)
from app.features.customer.dependencies.services.customer import (
    get_customer_service,
)
from app.features.customer.schemas.customer import (
    CustomerResponseSchema,
)

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)


@router.get(
    "/me",
    response_model=CustomerResponseSchema | None,
    status_code=status.HTTP_200_OK,
    summary="Get current customer",
)
async def get_current_customer(
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
    service: Annotated[
        CustomerService,
        Depends(get_customer_service),
    ],
) -> CustomerResponseSchema | None:

    if owner.user_id is not None:
        customer = await service.get_by_user_id(
            owner.user_id
        )
    else:
        customer = await service.get_by_session_id(
            owner.session_id
        )

    if customer is None:
        return None

    return CustomerResponseSchema.model_validate(
        customer
    )