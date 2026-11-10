
from typing import Annotated

from fastapi import Depends, status

from app.features.consents.consent_route import router
from app.features.consents.consent_service import ConsentService
from app.features.consents.dependencies.services import (
    get_consent_service,
)
from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)


@router.get(
    "/terms/status",
    status_code=status.HTTP_200_OK,
    summary="Check current terms acceptance",
)
async def get_terms_acceptance_status(
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
    service: Annotated[
        ConsentService,
        Depends(get_consent_service),
    ],
) -> bool:
    accepted = await service.has_accepted_current_terms(
        user_id=owner.user_id,
        session_id=owner.session_id,
    )

    return accepted