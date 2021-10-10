import os
import pytest

os.environ["TEST"] = "True"

from os.path import dirname

from sqlalchemy_utils import create_database, drop_database
from alembic.config import Config
from alembic import command
from app.models import database


@pytest.fixture(scope="module")
def test_db():
    create_database(database.TEST_DATABASE_URL)
    base_dir = dirname(dirname(dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    try:
        yield database.TEST_DATABASE_URL
    finally:
        # pass
        drop_database(database.TEST_DATABASE_URL)
