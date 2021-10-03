from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.utils import users, posts

auth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


async def get_current_user(token: str = Depends(auth2_scheme)):
    user = await users.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.get('is_active'):
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return user


async def get_post_by_id(post_id: int):
    post = await posts.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post