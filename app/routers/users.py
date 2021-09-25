from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import users
from app.utils import users as users_utils
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post('/user/create', response_model=users.User)
async def create_user(user: users.UserCreate):
    # Проверяем что в БД нету пользователя с таким email
    user_item = await users_utils.get_user_by_email(user.email)
    if user_item:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return await users_utils.create_user(user)


@router.post('/user/login', response_model=users.TokenBase)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not users_utils.validate_password(form_data.password, user.get('hashed_password')):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return await users_utils.create_user_token(user_id=user.get('id'))


@router.get('/user/info', response_model=users.UserBase)
async def user_info(current_user: users.User = Depends(get_current_user)):
    return current_user



