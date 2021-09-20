import string
import random
import hashlib
from datetime import datetime, timedelta
from app.models.users import users_table, token_table
from app.models.database import database
from app.schemas.users import UserCreate


async def get_user_by_email(email: str):
    query = users_table.select().where(users_table.c.email == email)
    print("\nget_user_by_email->>>")
    print(query)
    return await database.fetch_one(query)


async def create_user_token(user_id: int):
    query = (
        token_table.insert().values(
            user_id=user_id,
            ts_expires=datetime.now() + timedelta(weeks=2)
        ).returning(
            token_table.c.token, token_table.c.ts_expires
        )
    )
    print("\n\ncreate_user_token->>>")
    print(query)
    return await database.fetch_one(query)


async def create_user(user: UserCreate):
    """ Создаем нового пользователя """
    salt = get_random_string()
    print("salt", salt)
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        name=user.name, email=user.email, hashed_password=f'{salt}${hashed_password}'
    )
    print("\ncreate_user->>>")
    print(query)
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_result = {"token": token.get('token'), "ts_expires": token.get('ts_expires')}
    # Зачем "is_active": True ???
    # return {**user.dict(), "token": token_result, "user_id": user_id, "is_active": True}
    return {**user.dict(), "token": token_result, "user_id": user_id}


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str):
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


if __name__ == '__main__':
    # create_user(user=UserCreate(email="kpgkgwvenebkulgrfv@pp7rvv.com", name="dsa", password="321"))
    res = create_user_token(user_id=1)
    print("\n\n")
    print(res)
    print("\n\n")
