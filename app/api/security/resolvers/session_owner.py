from fastapi import Depends, Request
from dataclasses import dataclass
from app.api.security.resolvers.sessions import get_user_id
from app.api.security.exceptions import AuthException

@dataclass(frozen=True)
class OwnerSession:
    user_id: int | None = None
    session_id: str | None = None

    @property
    def is_user(self) -> bool:
        return self.user_id is not None
    
def get_anon_id(request: Request) -> int:
    anon_id = request.cookies.get("anon_session_id")
    if not anon_id:
        raise AuthException(
            "Missing authentication or anonymous session",
            {
                "resolver": "session_owner/security",
                "event": "get_session_owner"
            }
        )

    return anon_id

def get_session_owner(
    request: Request,
    user_id: int = Depends(get_user_id)
) -> OwnerSession:
    if user_id is not None:
        return OwnerSession(user_id=user_id)

    return OwnerSession(
        session_id=get_anon_id(request)
        )