from app.features.mail.providers.resend import (
    ResendMailProvider,
)
from app.features.mail.providers.base import (
    MailProvider,
)

def get_mail_provider() -> MailProvider:
    return ResendMailProvider()