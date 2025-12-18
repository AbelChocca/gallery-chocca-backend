from abc import ABC, abstractmethod

class HashRepository(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str)-> bool:
        pass