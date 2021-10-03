from fastapi import APIRouter, Depends

from app.schemas.users import User
from app.schemas.posts import PostModel, PostDetailsModel
from app.utils.dependencies import get_current_user
import app.utils.posts as post_utils

router = APIRouter()


@router.post('/post/create', response_model=PostDetailsModel)
async def create_post(post: PostModel, current_user: User = Depends(get_current_user)):
    post = await post_utils.create_post(post, current_user)
    return post

