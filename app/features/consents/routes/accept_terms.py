from typing import Annotated

from fastapi import Depends, status

from app.features.consents.consent_route import router
from app.features.consents.consent_service import ConsentService
from app.features.consents.consent_schema import (
    ConsentResponseSchema,
)
from app.features.consents.dependencies.services import (
    get_consent_service,
)
from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

@router.post(
    "/terms",
    response_model=ConsentResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Accept current terms and conditions",
)
async def accept_terms(
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    service: Annotated[
        ConsentService,
        Depends(get_consent_service),
    ],
) -> ConsentResponseSchema:

    result = await service.accept_terms(
        user_id=owner.user_id,
        session_id=owner.session_id,
    )

    return ConsentResponseSchema.model_validate(result)