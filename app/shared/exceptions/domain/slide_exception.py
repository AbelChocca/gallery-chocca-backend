from app.shared.exceptions.domain.domain_exception import DomainException

class SlideNotFound(DomainException):
    def __init__(self, message: str, status_code = 404):
        super().__init__(message, status_code)