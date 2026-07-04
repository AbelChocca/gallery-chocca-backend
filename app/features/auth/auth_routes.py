from app.features.auth.auth_route import router
from app.api.security.rate_limiter.ratelimiter import limiter
from app.features.auth.schema import RegisterUserSchema, ReadSessionSchema, LoginUserSchema
from app.features.auth.dto import LoginUserCommand, RegisterUserCommand
from app.api.security.resolvers.session_owner import get_anon_id
from app.api.security.resolvers.captcha_resolver import verify_captcha
from app.api.security.resolvers.sessions import get_user_session
from app.features.auth.auth_service import AuthService
from app.features.auth.dependency import get_auth_service

from fastapi import status, Depends
from typing import Annotated

@router.post(
    path='/login',
    dependencies=[Depends(limiter.limiter(limit=10, window=60))],
    status_code=status.HTTP_200_OK,
    summary='Login endpoint'
)
async def login(
    login_schema: LoginUserSchema,
    service: Annotated[AuthService, Depends(get_auth_service)],
    anon_id: Annotated[int, Depends(get_anon_id)]
) -> dict[str, str]:
    return await service.login_user(LoginUserCommand(**login_schema.model_dump()), anon_id)

@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    summary='Logout endpoint for users'
)
async def logout(
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> dict:
    return service.logout_user()

@router.post(
    '/register',
    response_model=ReadSessionSchema,
    dependencies=[Depends(limiter.limiter(3, 60))],
    status_code=status.HTTP_201_CREATED,
    summary='Register form for user'
    )
async def register_user(
    register_schema: Annotated[RegisterUserSchema, Depends(verify_captcha)],
    service: Annotated[AuthService, Depends(get_auth_service)],
    anon_id: Annotated[int, Depends(get_anon_id)]
) -> ReadSessionSchema:
    command = RegisterUserCommand(
        name=register_schema.name,
        email=register_schema.email,
        password=register_schema.password
    )
    res = await service.register_user(command, anon_id)
    return ReadSessionSchema(**res)

@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=ReadSessionSchema | None,
    summary="Endpoint for user's info"
)
async def get_info(
    user: Annotated[ReadSessionSchema | None, Depends(get_user_session)]
) -> ReadSessionSchema | None:
    return user