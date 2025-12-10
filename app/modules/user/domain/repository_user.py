from abc import ABC, abstractmethod
from typing import Optional

from app.modules.user.domain.user import User

class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """
        If user exists, this method update it.
        """
        pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        pass