from fastapi import Depends, Request
from dataclasses import dataclass
from app.api.security.resolvers.sessions import get_user_id
from app.core.exceptions import ValidationError

@dataclass(frozen=True)
class OwnerSession:
    user_id: int | None = None
    session_id: str | None = None

    @property
    def is_user(self) -> bool:
        return self.user_id is not None

    @property
    def is_empty(self) -> bool:
        return self.user_id is None and self.session_id is None
    
def get_anon_id(request: Request) -> str | None:
    return getattr(request.state, "anon_session_id", None)

def get_session_owner(
    request: Request,
    user_id: int = Depends(get_user_id)
) -> OwnerSession:

    if user_id is not None:
        return OwnerSession(
            user_id=user_id
        )

    session_id = get_anon_id(request)

    if session_id is None:
        raise ValidationError(
            "Owner session is required"
        )

    return OwnerSession(
        session_id=session_id
    )