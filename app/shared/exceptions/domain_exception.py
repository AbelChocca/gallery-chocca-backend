class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.status_code =status_code
        self.message = message
        super().__init__(message)