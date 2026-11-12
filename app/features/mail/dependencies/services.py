from typing import Annotated

from fastapi import Depends

from app.features.mail.providers.base import (
    MailProvider,
)
from app.features.mail.services.mail_service import (
    MailService,
)
from app.features.mail.dependencies.provider import get_mail_provider

def get_mail_service(
    provider: Annotated[
        MailProvider,
        Depends(get_mail_provider),
    ],
) -> MailService:
    return MailService(
        provider=provider,
    )