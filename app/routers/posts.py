from fastapi import APIRouter, Depends, HTTPException, status

import app.utils.posts as post_utils
from app.schemas.users import User
from app.schemas.posts import PostModel, PostDetailsModel
from app.utils.dependencies import get_current_user, get_post_by_id

router = APIRouter()


@router.post(
    "/post/create", response_model=PostDetailsModel, status_code=status.HTTP_201_CREATED
)
async def create_post(post: PostModel, current_user: User = Depends(get_current_user)):
    post = await post_utils.create_post(post, current_user)
    return post


@router.get("/post/get/{post_id}", response_model=PostDetailsModel)
async def get_post(post_id: int, post: PostDetailsModel = Depends(get_post_by_id)):
    return post


@router.get("/post/list")
async def list_post(page: int = 1):
    total_count = await post_utils.get_count_posts()
    posts = await post_utils.get_posts(page)
    return {"total_count": total_count, "list": posts}


@router.post("/post/update/{post_id}", response_model=PostDetailsModel)
async def update_post(
    post_id: int,
    post_data: PostModel,
    current_user: User = Depends(get_current_user),
    post: PostDetailsModel = Depends(get_post_by_id),
):
    if post.get("user_id") != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Access Denied")
    await post_utils.update_post(post_id, post_data)
    post = await post_utils.get_post(post_id)
    return post


@router.delete("/post/delete/{post_id}")
async def delete_post(post_id: int, post: PostDetailsModel = Depends(get_post_by_id)):
    await post_utils.delete_post(post_id)
    return {"success": 1}
