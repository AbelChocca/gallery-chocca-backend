from typing import Any, Optional, Dict, Protocol

class JWTProtocole(Protocol):
    def generate_token(self, data: dict, refresh: Optional[bool] = False) -> str:
        ...

    def set_cookie(
            self, 
            key: str,
            token: str,
            expires: int
            ) -> None:
        """
        Set an cookie by key, token and expires (in seconds)
        
        :param self: Default
        :param key: key of the cookie httponly
        :type key: str
        :param token: encoded token of the cookie
        :type token: str
        :param expires: time to expire the cookie
        :type expires: int
        """
        ...

    def renew_tokens_and_get_access_payload(self, refresh_token: str) -> Dict[str, Any]:
        ...
    
    def get_token_from_cookies(self) -> Dict[str, Any]:
        ...

    def verify_token(self, token: str) -> Dict[str, Any]:
        ...

    def delete_cookie(self, key: str) -> None:
        ...