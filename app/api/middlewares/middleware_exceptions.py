
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import traceback

from app.core.app_exception import AppException
from app.core.log.config import logger_service
from app.core.settings.pydantic_settings import settings

IS_DEV = settings.ENV == "development"


class MiddlewareException:

    def register(self, app: FastAPI):

        @app.middleware("http")
        async def exception_middleware(
            request: Request,
            call_next,
        ):
            try:
                return await call_next(request)

            except AppException as exc:
                original = exc.__cause__

                context = {
                    **(exc.context or {}),
                    "method": request.method,
                    "path": request.url.path,
                    "error_code": exc.error_code,
                }

                if original is not None:
                    context["original_exception_type"] = type(original).__name__

                    if IS_DEV:
                        context["original_exception_message"] = str(original)

                    logger_service.opt(
                        exception=exc if IS_DEV else None,
                    ).log(
                        exc.log_level,
                        exc.message,
                        **context,
                    )
                else:
                    logger_service.log(
                        exc.log_level,
                        exc.message,
                        **context,
                    )

                return JSONResponse(
                    status_code=exc.status_code,
                    content={"detail": exc.message},
                )

            except Exception as exc:
                tb = exc.__traceback__
                last = (
                    traceback.extract_tb(tb)[-1]
                    if tb
                    else None
                )

                logger_service.opt(
                    exception=exc,
                ).error(
                    "Unknown internal server error",
                    method=request.method,
                    path=request.url.path,
                    status_code=500,
                    exception_type=type(exc).__name__,
                    exception_message=str(exc),
                    origin_file=getattr(
                        last, "filename", None
                    ),
                    origin_line=getattr(
                        last, "lineno", None
                    ),
                    origin_function=getattr(
                        last, "name", None
                    ),
                )

                return JSONResponse(
                    status_code=500,
                    content={
                        "detail": "Internal server error"
                    },
                )
