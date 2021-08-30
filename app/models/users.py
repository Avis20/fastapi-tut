import sqlalchemy.sql.expression
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    MetaData,
    Column,
    Table,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("email", String(40), unique=True, index=True),
    Column("hashed_password", String()),
    Column("is_active", Boolean(), server_default=sqlalchemy.sql.expression.true(), nullable=False)
)

token_table = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "token",
        UUID(),
        server_default=sqlalchemy.text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True
    ),
    Column("ts_expires", DateTime),
    Column("user_id", Integer, ForeignKey("users.id"))
)
