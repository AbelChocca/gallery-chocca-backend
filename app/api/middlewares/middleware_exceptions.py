from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.shared.exceptions.domain_exception import DomainException
from app.shared.exceptions.infraestructure_exception import InfraestructureException
from app.shared.exceptions.application_exception import ApplicationException

from app.core.log.config import logger_service

class MiddlewareException:
    def register(self, app: FastAPI):
        @app.middleware("http")
        async def exception_middleware(request: Request, call_next):
            try:
                return await call_next(request)
            except DomainException as d:
                logger_service.error(f"Domain exception from: {str(d.message)}")
                return JSONResponse(
                    status_code=d.status_code,
                    content={"detail": d.message}
                )
            except InfraestructureException as i:
                logger_service.error(f"Internal server error from: {str(i.message)}")
                return JSONResponse(
                    status_code=i.status_code,
                    content={'detail': i.message}
                )
            except ApplicationException as a:
                logger_service.error(f"Application error from {str(a.message)}")
                return JSONResponse(
                    status_code=a.status_code,
                    content={'defailt': a.message}
                )
            except Exception as e:
                logger_service.error(f"Unknow internal server error: {str(e)}")
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Internal server error"}
                )