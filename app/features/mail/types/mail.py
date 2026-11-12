# app/features/mail/types/mail.py

from dataclasses import dataclass


@dataclass
class MailAttachmentDTO:
    filename: str
    content: bytes


@dataclass
class SendMailDTO:
    to: str
    subject: str
    html: str

    attachments: list[MailAttachmentDTO] | None = None

    from_email: str | None = None
    reply_to: str | None = None


@dataclass
class SentMailDTO:
    id: str