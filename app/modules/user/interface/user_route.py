from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['user', 'login', 'auth'])

from app.modules.user.interface.endpoints import get_info, login, logout, register, get_admin_session