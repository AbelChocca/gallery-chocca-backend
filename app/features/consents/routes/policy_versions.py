from fastapi import status

from app.features.consents.consent_route import router
from app.features.consents.config.policy_versions import (
    POLICY_VERSIONS,
)
from app.features.consents.consent_schema import (
    PolicyVersionsResponse,
)


@router.get(
    "/policies/versions",
    response_model=PolicyVersionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current legal policy versions",
)
async def get_policy_versions() -> PolicyVersionsResponse:
    return PolicyVersionsResponse(
        terms=POLICY_VERSIONS.terms,
        privacy=POLICY_VERSIONS.privacy,
        cookies=POLICY_VERSIONS.cookies,
    )