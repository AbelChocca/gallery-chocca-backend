from app.infra.exceptions import InfraestructureException

class CloudinaryException(InfraestructureException):
    def __init__(self, message, status_code = 500):
        super().__init__(message, status_code)