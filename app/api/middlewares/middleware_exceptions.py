from fastapi import FastAPI, Request
import traceback
from fastapi.responses import JSONResponse
from app.core.app_exception import AppException

from app.core.log.config import logger_service

class MiddlewareException:
    def register(self, app: FastAPI):
        @app.middleware("http")
        async def exception_middleware(request: Request, call_next):
            try:
                return await call_next(request)
            except AppException as a:
                logger_service.log(
                    a.log_level,
                    a.message,
                    error=str(a),
                    error_code=a.error_code,
                    **a.context,
                    method=request.method,
                    path=request.url.path,
                )
                return JSONResponse(
                    status_code=a.status_code,
                    content={"detail": a.message}
                )
            except Exception as e:
                tb = e.__traceback__
                last = traceback.extract_tb(tb)[-1] if tb else None

                logger_service.opt(exception=e).error(
                    "Unknow internal server error",
                    method=request.method,
                    path=request.url.path,
                    status_code=500,
                    exception_type=type(e).__name__,
                    exception_message=str(e),
                    origin_file=getattr(last, "filename", None),
                    origin_line=getattr(last, "lineno", None),
                    origin_function=getattr(last, "name", None),
                )
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Internal server error"}
                )