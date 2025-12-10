import re
from typing import Optional

from app.shared.exceptions.domain.user_exception import (
    InvalidEmailFormatException, 
    PasswordTooShortException, 
    EmailTooShortException, 
    SameEmailError
)

class User:
    def __init__(
            self,
            name: str,
            email: str,
            hashed_password: str,
            role: str = 'user',
            id: Optional[int] = None
            ):
        
        self._verify_email(
            email=email
        )
        self._verify_password(password=hashed_password)
        
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.hashed_password = hashed_password

    def change_email(self, new_email: str) -> None:
        self._verify_email(email=new_email)

        if (self.email == new_email):
            raise SameEmailError()

        self.email = new_email

    def change_password(self, new_hashed_password: str)-> None:
        self.hashed_password = new_hashed_password
    
    @staticmethod
    def _verify_email(email: str) -> None:
        if (len(email) < 8):
            raise EmailTooShortException()
        
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
            raise InvalidEmailFormatException()

    @staticmethod
    def _verify_password(password: str) ->None:
        if len(password) < 8:
            raise PasswordTooShortException()
        