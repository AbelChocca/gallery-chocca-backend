from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])

from app.api.security.auth import auth_routes

