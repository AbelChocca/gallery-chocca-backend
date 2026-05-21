from fastapi import APIRouter

router = APIRouter(prefix='/v1/user', tags=['user'])

from app.features.user.routes import get_info, get_user_by_id, get_users