from abc import ABC, abstractmethod

from app.modules.mail.domain.entitites.base_email import BaseEmail

class EmailRepository(ABC):
    @abstractmethod
    async def save(self, email: BaseEmail) -> BaseEmail:
        pass

    @abstractmethod
    async def delete(self, email_id: int) -> None:
        pass