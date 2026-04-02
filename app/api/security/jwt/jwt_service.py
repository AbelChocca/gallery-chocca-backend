from app.api.security.jwt.protocole import JWTProtocole
from app.core.settings.pydantic_settings import get_settings, Settings
from app.api.security.jwt.jwt_exception import JWTException
from app.core.exceptions import ValueNotFound

from fastapi import Request, Response, Depends
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Dict, Any, Optional

class JWTRepositoryInfra(JWTProtocole):
    def __init__(self, request: Request, response: Response, settings: Settings):
        self.request = request
        self.response = response
        self.settings = settings

    def renew_tokens_and_get_access_payload(self, refresh_token: str) -> Dict[str, Any]:
        refresh_payload = self.verify_token(refresh_token)

        user_data = {"sub": refresh_payload.get("sub"), "role": refresh_payload.get("role")}
        new_access_token = self.generate_token(data=user_data)
        new_refresh_token = self.generate_token(data=user_data, refresh=True)

        self.delete_cookie("refresh_token")
        
        self.set_cookie(
            key="session_token",
            token=new_access_token,
            expires=self.settings.ACCESS_TOKEN_EXPIRES_SECONDS
            )
        self.set_cookie(
            key="refresh_token",
            token=new_refresh_token,
            expires=self.settings.REFRESH_TOKEN_EXPIRES_SECONDS
            )
        
        return self.verify_token(new_access_token)
    
    def get_session_token_from_cookies_with_no_raises(self) -> str | None:
        return self.request.cookies.get("session_token")

    def get_token_from_cookies(self) -> Dict[str, Any]:
        session_token = self.request.cookies.get("session_token")
        if session_token:
            return self.verify_token(session_token)
        
        refresh_token = self.request.cookies.get("refresh_token")
        if refresh_token:
            try:
                return self.renew_tokens_and_get_access_payload(refresh_token)
            except JWTException as e:
                self.delete_cookie("refresh_token")
                raise e
        raise ValueNotFound(
            "Token not found",
            {
                "service": "JWT/security",
                "event": "get_token_from_cookies"
            }
        )
    
    def generate_token(self, data: dict, refresh: Optional[bool] = False):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (timedelta(seconds=self.settings.REFRESH_TOKEN_EXPIRES_SECONDS) if refresh else timedelta(seconds=self.settings.ACCESS_TOKEN_EXPIRES_SECONDS))
        to_encode.update({ 'exp': expire })
        
        try:
            encoded_jwt = jwt.encode(to_encode, self.settings.SECRET_KEY, algorithm=self.settings.TOKEN_ALGORITHM)
            return encoded_jwt
        except JWTError as e:
            raise JWTException("Error to encoding the data.") from e
        
    def set_cookie(
            self, 
            key: str,
            token: str,
            expires: int
            ) -> None:
        is_prod = self.settings.ENV == "production"
        self.response.set_cookie(
            key=key,
            value=token,
            max_age=expires,
            expires=timedelta(seconds=expires),
            path='/',
            secure=is_prod,
            httponly=True,
            samesite='strict' if is_prod else 'lax'
        )

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, key=self.settings.SECRET_KEY, algorithms=[self.settings.TOKEN_ALGORITHM])

            return payload
        except ExpiredSignatureError as e:
            raise JWTException(
                "The token expired",
                {
                    "service": "JWT/security",
                    "event": "verify_token",
                }
            ) from e
        except JWTError as e:
            raise JWTException(
                "The token is invalid in any way.",
                {
                    "service": "JWT/security",
                    "event": "verify_token",
                }
            ) from e
        
    def delete_cookie(self, key: str) -> None:
        self.response.delete_cookie(key, '/')

def get_jwt_repo(
        request: Request, 
        response: Response, 
        settings: Settings = Depends(get_settings)
        ) -> JWTProtocole:
    return JWTRepositoryInfra(request, response, settings)