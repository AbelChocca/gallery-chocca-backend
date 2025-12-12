from app.modules.mail.domain.entitites.base_email import BaseEmail

from typing import Optional

class ReplyEmail(BaseEmail):
    def __init__(
            self, 
            subject: str, 
            from_email: str, 
            to_email: str, 
            content: str, 
            is_deleted: bool = False, 
            id: Optional[int] = None,
            head_email_id: Optional[int] = None,
            ):
        super().__init__(subject, from_email, to_email, content, is_deleted, id)
        self.head_email_id = head_email_id

    def delete_reply_email(self) -> None:
        self.is_deleted = True