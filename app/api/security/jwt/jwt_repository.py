from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

class JWTRepository(ABC):
    @abstractmethod
    def generate_token(self, data: dict, refresh: Optional[bool] = False) -> str:
        pass

    @abstractmethod
    def set_jwt_cookie(self, token: str):
        pass

    @abstractmethod
    def set_refresh_token_cookie(self, refresh_token: str) -> None:
        pass

    @abstractmethod
    def renew_tokens_and_get_access_payload(self, refresh_token: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_token_from_cookies(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_session_cookie(self) -> None:
        pass

    @abstractmethod
    def delete_refresh_cookie(self) -> None:
        pass