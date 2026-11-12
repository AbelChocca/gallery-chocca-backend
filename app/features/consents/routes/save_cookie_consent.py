from typing import Annotated

from fastapi import Depends, status

from app.features.consents.consent_route import router
from app.features.consents.consent_service import ConsentService
from app.features.consents.types import CookiePreferencesDTO
from app.features.consents.consent_schema import (
    ConsentResponseSchema,
    SaveCookieConsentRequest,
)
from app.features.consents.dependencies.services import (
    get_consent_service,
)
from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)


@router.post(
    "/cookies",
    response_model=ConsentResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Save cookie preferences",
)
async def save_cookie_consent(
    body: SaveCookieConsentRequest,
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    service: Annotated[
        ConsentService,
        Depends(get_consent_service),
    ],
) -> ConsentResponseSchema:

    result = await service.save_cookies(
        user_id=owner.user_id,
        session_id=owner.session_id,
        preferences=CookiePreferencesDTO(
            analytics=body.preferences.analytics,
            marketing=body.preferences.marketing,
        ),
    )

    return ConsentResponseSchema.model_validate(result)