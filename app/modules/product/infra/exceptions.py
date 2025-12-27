from app.shared.exceptions.infraestructure_exception import InfraestructureException

class ProductNotFound(InfraestructureException):
    def __init__(self, message: str, status_code: int = 404):
        super().__init__(message, status_code)

class VariantProductNotFound(InfraestructureException):
    def __init__(self, message: str = "Variant not found", status_code = 404):
        super().__init__(message, status_code)

class VariantImageNotFound(InfraestructureException):
    def __init__(self, message: str = "Image not found.", status_code = 404):
        super().__init__(message, status_code)