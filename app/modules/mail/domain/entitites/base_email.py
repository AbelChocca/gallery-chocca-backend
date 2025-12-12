
from typing import Optional

class BaseEmail:
    def __init__(
            self,
            subject: str,
            from_email: str,
            to_email: str,
            content: str,
            is_deleted: bool = False,
            id: Optional[int] = None
            ):
        self.id = id
        self.is_deleted = is_deleted
        self.content = content
        self.to_email = to_email
        self.from_email = from_email
        self.subject = subject


    