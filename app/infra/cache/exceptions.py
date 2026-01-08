from app.infra.exceptions import InfraestructureException

class InternalCacheException(InfraestructureException):
    def __init__(self, message: str = "Cache Internal's error", status_code = 503):
        super().__init__(message, status_code)