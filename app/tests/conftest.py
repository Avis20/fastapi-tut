
import os
from os.path import dirname
import pytest

from sqlalchemy_utils import create_database
from alembic.config import Config
from alembic import command
from app.models import database

os.environ['TEST'] = 'True'


@pytest.fixture(scope="module")
def test_db():
    create_database(database.TEST_DATABASE_URL)
    base_dir = dirname(dirname(dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, 'alembic.ini'))
    command.upgrade(alembic_cfg, 'head')
    try:
        database.TEST_DATABASE_URL
    finally:
        print(111)


def test_1(test_db):
    assert 1 == 1