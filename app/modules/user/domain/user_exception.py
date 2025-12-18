from app.shared.exceptions.domain_exception import DomainException

class EmailTooShortException(DomainException):
    def __init__(self, message: str = "Email's value too short", status_code: int = 401):
        super().__init__(message, status_code)

class InvalidEmailFormatException(DomainException):
    def __init__(self, message: str = "Invalid email format", status_code: int = 401):
        super().__init__(message, status_code)

class PasswordTooShortException(DomainException):
    def __init__(self, message: str = "Password's value too short", status_code: int = 401):
        super().__init__(message, status_code)

class SameEmailError(DomainException):
    def __init__(self, message: str = "Current email is equal to the new email.", status_code: int = 401):
        super().__init__(message, status_code)

class SamePasswordError(DomainException):
    def __init__(self, message: str = "Current password is equal to the new password.", status_code: int = 401):
        super().__init__(message, status_code)

class UserNotFoundException(DomainException):
    def __init__(self, message: str, status_code = 404):
        super().__init__(message, status_code)

class InvalidPassword(DomainException):
    def __init__(self, message: str = "Password incorrect, retry.", status_code = 400):
        super().__init__(message, status_code)