from fastapi import APIRouter, HTTPException
from app.schemas import users
from app.utils import users as users_utils

router = APIRouter()


@router.post('/user/create', response_model=users.User)
async def create_user(user: users.UserCreate):
    # Проверяем что в БД нету пользователя с таким email
    user_item = await users_utils.get_user_by_email(user.email)
    if user_item:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return await users_utils.create_user(user)
