from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])

from app.features.auth import auth_routes

