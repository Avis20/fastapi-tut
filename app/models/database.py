import databases
from os import getenv

DATABASE_URL = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"
database = databases.Database(DATABASE_URL)

TEST_DATABASE_URL = None

if getenv('TEST'):
    DB_NAME = 'test-db'
    TEST_DATABASE_URL = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{DB_NAME}"
    database = databases.Database(TEST_DATABASE_URL)
