from app.features.mail.providers.base import (
    MailProvider,
)
from app.features.mail.types.mail import (
    SendMailDTO,
    SentMailDTO,
)


class MailService:

    def __init__(
        self,
        provider: MailProvider,
    ) -> None:
        self._provider = provider

    async def send(
        self,
        *,
        payload: SendMailDTO,
    ) -> SentMailDTO:

        return await self._provider.send(
            payload
        )