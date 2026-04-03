from uuid import uuid4
from fastapi import FastAPI, Request, Response
from app.core.settings.pydantic_settings import settings

class AnonSessionIdMiddleware:
    def register(self, app: FastAPI):
        @app.middleware("http")
        async def check_anon_session(request: Request, call_next):
            session_id = request.cookies.get("anon_session_id")

            response: Response = await call_next(request)

            if not session_id:
                is_prod = settings.ENV == "production"

                session_id = str(uuid4())
                response.set_cookie(
                    key="anon_session_id",
                    value=session_id,
                    httponly=True,
                    secure=is_prod,   # True en prod
                    samesite="none" if is_prod else "lax",
                    path="/"
                )

            return response