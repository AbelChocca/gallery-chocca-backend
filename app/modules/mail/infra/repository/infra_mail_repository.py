from app.modules.mail.domain.repository.mail_repository import EmailRepository
from app.modules.mail.domain.entitites.base_email import BaseEmail
from app.modules.mail.domain.entitites.head_email import HeadEmail
from app.modules.mail.domain.entitites.reply_email import ReplyEmail
from app.modules.mail.infra.models.model_email import HeadEmailTable, ReplyEmailTable

from app.modules.mail.infra.mappers.email_mapper import InfraEmailMapper

from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, Type, Any, Callable

class InfraMailRepository(EmailRepository):
    def __init__(
            self,
            db_session: AsyncSession
            ):
        self.db_session: AsyncSession = db_session

        self.model_mappers: Dict[Type[Any], Callable[[Any], Any]] = {
            HeadEmail: InfraEmailMapper.to_head_table,
            ReplyEmail: InfraEmailMapper.to_reply_table,
            HeadEmailTable: InfraEmailMapper.to_head_entity,
            ReplyEmailTable: InfraEmailMapper.to_reply_entity
        }

    async def save(self, email: BaseEmail) -> BaseEmail:
        pass

    async def delete(self, email_id: int) -> None:
        pass