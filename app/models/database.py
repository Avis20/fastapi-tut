import databases
from os import getenv

DATABASE_URL = (
    f"postgres://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"
)
database = databases.Database(DATABASE_URL)
