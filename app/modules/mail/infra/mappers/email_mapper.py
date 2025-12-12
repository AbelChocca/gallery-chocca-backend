from app.modules.mail.domain.entitites.head_email import HeadEmail
from app.modules.mail.domain.entitites.reply_email import ReplyEmail
from app.modules.mail.infra.models.model_email import HeadEmailTable, ReplyEmailTable

class InfraEmailMapper:
    @staticmethod
    def to_head_table(head_email: HeadEmail) -> HeadEmailTable:
        pass

    @staticmethod
    def to_reply_table(reply_email: ReplyEmail) -> ReplyEmailTable:
        pass

    @staticmethod
    def to_head_entity(head_email_table: HeadEmailTable) -> HeadEmail:
        pass

    @staticmethod
    def to_reply_entity(reply_email_table: ReplyEmailTable) -> ReplyEmail:
        pass