from typing import Protocol

class HashProtocole(Protocol):
    def hash(self, password: str) -> str:
        pass

    def verify(self, password: str, hashed_password: str)-> bool:
        pass