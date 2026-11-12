from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

from app.features.payments.payment_route import router

from app.features.payments.dependencies.use_cases.create_card_charge import (
    get_create_card_charge_use_case,
)

from app.features.payments.schemas.payment_schema import (
    CreateCardChargeRequestSchema,
    CreateCardChargeResponseSchema,
)

from app.features.payments.use_cases.create_card_charge import (
    CreateCardChargeUseCase,
)
from app.api.security.resolvers.client_ip import get_client_ip
from app.api.security.rate_limiter.ratelimiter import limiter

@router.post(
    "/{order_id}/charge",
    response_model=CreateCardChargeResponseSchema,
    dependencies=[Depends(limiter.limiter(5, 60))],
    status_code=status.HTTP_200_OK,
    summary="Create Openpay card charge",
)
async def create_card_charge(
    order_id: int,
    payload: CreateCardChargeRequestSchema,
    client_ip: Annotated[
        str,
        Depends(get_client_ip),
    ],
    use_case: Annotated[
        CreateCardChargeUseCase,
        Depends(get_create_card_charge_use_case),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
) -> CreateCardChargeResponseSchema:

    result = await use_case.execute(
        order_id=order_id,
        token_id=payload.token_id,
        device_session_id=payload.device_session_id,
        client_ip=client_ip,
        user_id=owner.user_id,
        session_id=owner.session_id,
    )

    return CreateCardChargeResponseSchema.model_validate(
        result
    )