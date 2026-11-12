
from typing import Annotated

from fastapi import Depends

from app.core.settings.pydantic_settings import Settings, get_settings

from app.features.complaints.types.complaint import (
    ComplaintProviderIdentity,
)

def get_complaint_provider(
    settings: Annotated[
        Settings,
        Depends(get_settings),
    ],
) -> ComplaintProviderIdentity:
    return ComplaintProviderIdentity(
        legal_name=settings.COMPLAINT_PROVIDER_LEGAL_NAME,
        ruc=settings.COMPLAINT_PROVIDER_RUC,
        address=settings.COMPLAINT_PROVIDER_ADDRESS,
    )
