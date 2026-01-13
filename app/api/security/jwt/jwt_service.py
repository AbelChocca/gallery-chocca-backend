from app.api.security.jwt.protocole import JWTProtocole
from app.core.log.protocole import LoggerProtocol
from app.core.log.loguru_service import get_logger_service
from app.core.settings.pydantic_settings import get_settings
from app.api.security.jwt.jwt_exception import TokenNotFound, TokenExpired, ForceLoginError, JWTException

from pydantic_settings import BaseSettings
from fastapi import Request, Response, Depends
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Dict, Any, Optional

class JWTRepositoryInfra(JWTProtocole):
    def __init__(self, request: Request, response: Response, settings: BaseSettings, logger: LoggerProtocol):
        self.request = request
        self.response = response
        self.settings = settings
        self.logger = logger

    def renew_tokens_and_get_access_payload(self, refresh_token: str) -> Dict[str, Any]:
        refresh_payload = self.verify_token(refresh_token)

        user_data = {"sub": refresh_payload.get("sub"), "role": refresh_payload.get("role")}
        new_access_token = self.generate_token(data=user_data)
        new_refresh_token = self.generate_token(data=user_data, refresh=True)

        self.delete_refresh_cookie()
        
        self.set_jwt_cookie(new_access_token)
        self.set_refresh_token_cookie(new_refresh_token)
        
        return self.verify_token(new_access_token)

    def get_token_from_cookies(self) -> Dict[str, Any]:
        access_token = self.request.cookies.get("access_token")
        if access_token:
            try:
                return self.verify_token(access_token)
            except TokenExpired as e:
                self.logger.warning(f"The access_token was expired: {str(e)}")
                self.delete_session_cookie()
                pass
            except JWTError as j:
                self.logger.error(f"Fatal error while verify the access token: {str(j)}")
                self.delete_session_cookie()
                raise j
        
        refresh_token = self.request.cookies.get("refresh_token")
        if refresh_token:
            try:
                return self.renew_tokens_and_get_access_payload(refresh_token)
            except TokenExpired as e:
                self.logger.warning(f"The refresh token was expired: {str(e)}")
                self.delete_refresh_cookie()
                raise ForceLoginError() from e
            except JWTError as j:
                self.logger.error(f"Fatal error while verify the refresh token: {str(j)}")
                self.delete_refresh_cookie()
                raise j
        raise TokenNotFound()
    
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
        self.response.set_cookie(
            key=key,
            value=token,
            max_age=expires,
            expires=timedelta(seconds=expires),
            path='/',
            secure=False, # Aun no estamos en produccion
            httponly=True,
            samesite='lax'
        )

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, key=self.settings.SECRET_KEY, algorithms=[self.settings.TOKEN_ALGORITHM])

            return payload
        except ExpiredSignatureError as e:
            raise TokenExpired("The token was expire") from e
        except JWTError as e:
            raise JWTException("The token is invalid in any way.") from e
        
    def delete_cookie(self, key: str) -> None:
        self.response.delete_cookie(key, '/')

def get_jwt_repo(
        request: Request, 
        response: Response, 
        settings: BaseSettings = Depends(get_settings), 
        logger: LoggerProtocol = Depends(get_logger_service)
        ) -> JWTProtocole:
    return JWTRepositoryInfra(request, response, settings, logger)