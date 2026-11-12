from abc import ABC, abstractmethod

from app.features.mail.types.mail import (
    SendMailDTO,
    SentMailDTO,
)


class MailProvider(ABC):

    @abstractmethod
    async def send(
        self,
        payload: SendMailDTO,
    ) -> SentMailDTO:
        ...