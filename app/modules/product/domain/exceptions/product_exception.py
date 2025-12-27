from app.shared.exceptions.domain_exception import DomainException

class InvalidProductNameException(DomainException):
    def __init__(self, message: str = "Product name too short.", status_code = 401):
        super().__init__(message, status_code)
        
class MissingVariantsException(DomainException):
    def __init__(self, message: str = "Product must have at least one variant.", status_code: int = 401):
        super().__init__(message, status_code)

class InvalidDiscountPercentException(DomainException):
    def __init__(self, message: str = "Invalid discount percent.", status_code: int = 401):
        super().__init__(message, status_code)

class InvalidVariantImageException(DomainException):
    def __init__(self, message: str, status_code = 400):
        super().__init__(message, status_code)

class CannotDeleteVariantProduct(DomainException):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)
