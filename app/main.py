import uvicorn
from fastapi import FastAPI
from app.routers import users, posts, healthcheck
from app.models.database import database
from sqlalchemy.sql import select

app = FastAPI()


@app.on_event("startup")
async def startup():
    # при запуске приложения коннектимся к БД
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # при отключении - дисконект
    await database.disconnect()


@app.get("/")
def get_root():
    return {"success": 1}


@app.get('/test_select')
async def test_select():
    """ Проверка подключения к БД """
    response = await database.execute(select([1]))
    print(response)
    return 1

app.include_router(healthcheck.router)
app.include_router(users.router)
app.include_router(posts.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
