from datetime import datetime

from pydantic import BaseModel


class PostModel(BaseModel):
    """ Базовая модель поста """
    title: str
    content: str


class PostDetailsModel(PostModel):
    id: int
    ts_create: datetime
    user_name: str
