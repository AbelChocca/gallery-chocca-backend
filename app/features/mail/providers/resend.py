import base64

import resend

from resend.exceptions import ResendError

from app.core.settings.pydantic_settings import (
    settings,
)

from app.features.mail.providers.base import (
    MailProvider,
)
from app.features.mail.types.mail import (
    SendMailDTO,
    SentMailDTO,
)
from app.features.mail.exceptions import (
    MailProviderError,
)


class ResendMailProvider(MailProvider):

    def __init__(self) -> None:
        resend.api_key = settings.RESEND_API_KEY

    async def send(
        self,
        payload: SendMailDTO,
    ) -> SentMailDTO:

        params: resend.Emails.SendParams = {
            "from": payload.from_email or settings.RESEND_FROM_EMAIL,
            "to": [payload.to],
            "subject": payload.subject,
            "html": payload.html,
        }

        if payload.reply_to:
            params["reply_to"] = payload.reply_to

        if payload.attachments:
            params["attachments"] = [
                {
                    "filename": attachment.filename,
                    "content": base64.b64encode(
                        attachment.content
                    ).decode("utf-8"),
                }
                for attachment
                in payload.attachments
            ]

        try:
            response = await resend.Emails.send_async(
                params
            )

        except ResendError as exc:
            raise MailProviderError(
                message=(
                    "No se pudo enviar el correo "
                    "mediante Resend."
                ),
                context={
                    "provider": "resend",
                    "code": exc.code,
                    "type": exc.error_type,
                    "message": exc.message,
                },
            ) from exc

        return SentMailDTO(
            id=response["id"],
        )