from app.api.middlewares.middleware_exceptions import MiddlewareException
from app.api.middlewares.middleware_correlation_id import CorrelationIdMiddleware

from fastapi import FastAPI

class MiddlewareManager:
    def __init__(self, app: FastAPI):
        self.app = app
        self.middlewares = [
            MiddlewareException(),
            CorrelationIdMiddleware()
        ]
        self._register_all()

    def _register_all(self):
        for middleware in self.middlewares:
            middleware.register(self.app)

def init_middlewares(app: FastAPI) -> MiddlewareManager:
    return MiddlewareManager(app)