from typing import Annotated

from fastapi import Depends, status

from app.features.consents.consent_route import router
from app.features.consents.consent_service import ConsentService
from app.features.consents.consent_schema import (
    ConsentSummaryResponseSchema,
)
from app.features.consents.dependencies.services import (
    get_consent_service,
)
from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)



@router.get(
    "/me",
    response_model=ConsentSummaryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current consent preferences",
)
async def get_my_consents(
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    service: Annotated[
        ConsentService,
        Depends(get_consent_service),
    ],
) -> ConsentSummaryResponseSchema:

    result = await service.get_summary(
        user_id=owner.user_id,
        session_id=owner.session_id,
    )

    return ConsentSummaryResponseSchema.model_validate(result)



