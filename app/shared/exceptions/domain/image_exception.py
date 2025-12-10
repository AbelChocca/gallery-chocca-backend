from app.shared.exceptions.domain.domain_exception import DomainException


class ImageNotFound(DomainException):
    def __init__(self, message: str = "Image not found.", status_code = 404):
        super().__init__(message, status_code)

class CannotDeleteImage(DomainException):
    def __init__(self, message: str, status_code = 400):
        super().__init__(message, status_code)