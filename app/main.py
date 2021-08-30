import uvicorn
from fastapi import FastAPI
import databases
from os import getenv
from models.posts import posts_table
from models.users import users_table
from sqlalchemy.sql import select

app = FastAPI()
DATABASE_URL = (
    f"postgres://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"
)
database = databases.Database(DATABASE_URL)


@app.on_event('startup')
async def startup():
    # при запуске приложения коннектимся к БД
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    # при отключении - дисконект
    await database.disconnect()


@app.get('/')
async def get_root():
    query = (
        select([
            posts_table.c.id,
            posts_table.c.title,
            posts_table.c.content,
            posts_table.c.ts_create,
            posts_table.c.user_id,
            users_table.c.name.label('username'),
        ])
        .select_from(posts_table.join(users_table))
    )
    print(query)
    return await database.fetch_all(query)


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
