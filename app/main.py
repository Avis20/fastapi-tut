import uvicorn
from fastapi import FastAPI
from app.models.posts import posts_table
from app.models.users import users_table
from sqlalchemy.sql import select
from app.routers import users
from app.models.database import database

app = FastAPI()


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

app.include_router(users.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
