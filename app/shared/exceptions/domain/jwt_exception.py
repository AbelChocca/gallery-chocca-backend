from app.shared.exceptions.domain.domain_exception import DomainException

class TokenNotFound(DomainException):
    def __init__(self, message = "Token from cookies wasn't found.", status_code = 404):
        super().__init__(message, status_code)

class TokenExpired(DomainException):
    def __init__(self, message = "Token was expired.", status_code = 401):
        super().__init__(message, status_code)
    
class ForceLoginError(DomainException):
    def __init__(self, message: str = "Session expired.", status_code = 401):
        super().__init__(message, status_code)

class ForbiddenException(DomainException):
    def __init__(self, message: str = "Oops...", status_code = 403):
        super().__init__(message, status_code)

class Unauthorized(DomainException):
    def __init__(self, message: str = "Please login.", status_code = 403):
        super().__init__(message, status_code)