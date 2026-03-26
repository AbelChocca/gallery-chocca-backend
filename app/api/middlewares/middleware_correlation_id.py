from uuid import uuid4
import time
from fastapi import Request, FastAPI, Response

from app.core.log.config import request_id_var, logger_service

class CorrelationIdMiddleware:
    def register(self, app: FastAPI):
        @app.middleware("http")
        async def correlation_id_middleware(request: Request, call_next):
            request_id = request.headers.get("X-Request-ID", str(uuid4()))
            token = request_id_var.set(request_id)

            start_time = time.perf_counter()
            try:
                response: Response = await call_next(request)
                
            finally:
                duration_ms = (time.perf_counter() - start_time) * 1000

                status_code = getattr(locals().get("response", None), "status_code", 500)

                logger_service.info(
                    "Request completed",
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code,
                    duration_ms=round(duration_ms, 2),
                )

                request_id_var.reset(token)

            response.headers["X-Request-ID"] = request_id
            return response
