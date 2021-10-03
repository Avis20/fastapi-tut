from datetime import datetime
from sqlalchemy.sql import select, desc, func

import app.schemas.posts as post_schema
from app.models.posts import posts_table
from app.models.users import users_table
from app.models.database import database


async def create_post(post: post_schema.PostModel, user):
    query = (
        posts_table.insert()
        .values(
            title=post.title,
            content=post.content,
            ts_create=datetime.now(),
            user_id=user.get("id"),
        )
        .returning(
            posts_table.c.id,
            posts_table.c.title,
            posts_table.c.content,
            posts_table.c.ts_create,
        )
    )
    print("\n\ncreate_post->>>\n")
    print(query)
    post = await database.fetch_one(query)
    # объект post возвращает ключи, post.values - значения
    # zip и dict превращают в словарь
    post = dict(zip(post, post.values()))
    post["user_name"] = user.get("name")
    return post


async def get_post(post_id):
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.ts_create,
                posts_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(posts_table.join(users_table))
        .where(posts_table.c.id == post_id)
    )
    print("\n\nget_post->>>\n")
    print(query)
    post = await database.fetch_one(query)
    return post


async def get_posts(page: int):
    records_per_page = 3
    offset = (page - 1) * records_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.ts_create,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(posts_table.join(users_table))
        .order_by(desc(posts_table.c.ts_create))
        .limit(records_per_page)
        .offset(offset)
    )
    print("\n\nget_posts->>>\n")
    print(query)
    posts = await database.fetch_all(query)
    return posts


async def get_count_posts():
    query = select([func.count()]).select_from(posts_table)
    print("\n\nget_count_posts->>>\n")
    print(query)
    total = await database.fetch_val(query)
    return total


async def update_post(post_id, post):
    query = (
        posts_table.update()
        .where(posts_table.c.id == post_id)
        .values(title=post.title, content=post.content)
    )
    print("\n\nupdate_posts->>>\n")
    print(query)
    post = await database.fetch_one(query)
    return post


async def delete_post(post_id):
    query = posts_table.delete().where(posts_table.c.id == post_id)
    print("\n\ndelete_post->>>\n")
    print(query)
    await database.fetch_one(query)
