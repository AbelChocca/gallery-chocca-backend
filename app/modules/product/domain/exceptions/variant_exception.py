from app.shared.exceptions.domain_exception import DomainException

class ColorTooShortException(DomainException):
    def __init__(self, message: str = "Color's value too short", status_code: int = 401):
        super().__init__(message, status_code)

class MissingSizesException(DomainException):
    def __init__(self, message: str ="Variant must have at least one size", status_code: int = 401):
        super().__init__(message, status_code)

class InvalidImageVariantMapping(DomainException):
    def __init__(self, message: str, status_code = 400):
        super().__init__(message, status_code)