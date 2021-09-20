from sqlalchemy import (
    Column,
    MetaData,
    Table,
    Integer,
    String,
    ForeignKey,
    DateTime,
)

from app.models.users import users_table

metadata = MetaData()

# Указываем связь с user через import
# т.к. просто "user.id" не увидит

posts_table = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column("content", String()),
    Column("ts_create", DateTime()),
    Column("user_id", Integer, ForeignKey(users_table.c.id))
)