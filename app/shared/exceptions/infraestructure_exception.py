class InfraestructureException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message,
        self.status_code = status_code
        super().__init__(message)

class DatabaseException(InfraestructureException):
    def __init__(self, message, status_code = 500):
        super().__init__(message, status_code)

class JWTException(InfraestructureException):
    def __init__(self, message, status_code = 500):
        super().__init__(message, status_code)