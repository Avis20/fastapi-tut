from datetime import datetime

import app.schemas.posts as post_schema
from app.models.posts import posts_table
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
    post = dict(zip(post, post.values()))
    post["user_name"] = user.get('name')
    return post

