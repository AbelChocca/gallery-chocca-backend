class ApplicationException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message: str = message
        self.status_code: int = status_code
        super().__init__(message)