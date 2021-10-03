from datetime import datetime
from sqlalchemy.sql import select

import app.schemas.posts as post_schema
from app.models.posts import posts_table
from app.models.users import users_table
from app.models.database import database


async def create_post(post: post_schema.PostModel, user):
    query = (
        posts_table.insert().values(
            title=post.title,
            content=post.content,
            ts_create=datetime.now(),
            user_id=user.get('id')
        ).returning(
            posts_table.c.id,
            posts_table.c.title,
            posts_table.c.content,
            posts_table.c.ts_create
        )
    )
    print("\n\ncreate_post->>>\n")
    print(query)
    post = await database.fetch_one(query)
    # объект post возвращает ключи, post.values - значения
    # zip и dict превращают в словарь
    post = dict(zip(post, post.values()))
    post["user_name"] = user.get('name')
    return post


async def get_post(post_id):
    query = (
        select([
            posts_table.c.id,
            posts_table.c.title,
            posts_table.c.content,
            posts_table.c.ts_create,
            users_table.c.name.label("user_name")
        ]).select_from(posts_table.join(users_table)).where(
            posts_table.c.id == post_id
        )
    )
    print("\n\nget_post->>>\n")
    print(query)
    post = await database.fetch_one(query)
    return post
