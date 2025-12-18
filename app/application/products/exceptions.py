from app.shared.exceptions.application_exception import ApplicationException

class MissMatchLength(ApplicationException):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)