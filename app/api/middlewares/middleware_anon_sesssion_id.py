from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from app.core.settings.pydantic_settings import settings

SESSION_PATHS = (
    "/cart",
    "/favorites",
    "/checkout",
    "/session/init",
    "/consents"
)

class AnonSessionIdMiddleware:
    def register(self, app: FastAPI):
        @app.middleware("http")
        async def check_anon_session(
            request: Request,
            call_next,
        ):

            is_public_policy_endpoint = (
                request.url.path == "/consents/policies/versions"
            )

            needs_session = (
                request.url.path.startswith(SESSION_PATHS)
                and not is_public_policy_endpoint
            )

            session_id = request.cookies.get("anon_session_id")

            try:
                session_id = str(UUID(session_id)) if session_id else None
            except (ValueError, AttributeError):
                session_id = None

            is_new = session_id is None

            if is_new and needs_session:
                session_id = str(uuid4())

            request.state.anon_session_id = session_id

            response = await call_next(request)

            if is_new and needs_session:
                response.set_cookie(
                    key="anon_session_id",
                    value=session_id,
                    httponly=True,
                    secure=settings.ENV == "production",
                    samesite="lax",
                    path="/",
                    domain=settings.COOKIE_DOMAIN or None,
                )

            return response