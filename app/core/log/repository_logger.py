from abc import ABC, abstractmethod

class LoggerRepository(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs) -> None:
        pass

    @abstractmethod
    def error(self, message: str, **kwargs) -> None:
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs) -> None:
        pass
