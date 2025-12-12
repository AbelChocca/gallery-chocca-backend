from app.modules.mail.domain.entitites.base_email import BaseEmail
from app.modules.mail.domain.entitites.reply_email import ReplyEmail

from typing import Optional, List

class HeadEmail(BaseEmail):
    def __init__(
            self, 
            subject: str, 
            from_email: str, 
            to_email: str, 
            content: str, 
            is_deleted: bool = False, 
            id: Optional[int] = None,
            reply_emails: Optional[List[ReplyEmail]] = None
        ):
        super().__init__(subject, from_email, to_email, content, is_deleted, id)
        self.reply_emails = reply_emails

    def set_deleted_email(self) -> None:
        self.is_deleted = True
        for reply in self.reply_emails:
            reply.delete_reply_email()