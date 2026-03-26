from fastapi import APIRouter

router = APIRouter(prefix='/v1/user', tags=['user', 'auth', 'v1'])

from app.api.v1.user.routes import get_admin_session, get_info, logout, register, login, get_user_by_id, get_users