from uuid import uuid4
from fastapi import Request, FastAPI

from app.core.log.config import request_id_var

class CorrelationIdMiddleware:
    def register(self, app: FastAPI):
        @app.middleware("http")
        async def correlation_id_middleware(request: Request, call_next):
            request_id = request.headers.get("X-Request-ID", str(uuid4()))
            if not request_id:
                request_id = str(uuid4)
            request_id_var.set(request_id)
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
