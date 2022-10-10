import pytest
from app import create_app
from pytest_postgresql import factories

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def db_session(postgresql):
    cur = postgresql.cursor()
    cur.execute(open("./project/schema.sql", "r").read())
    postgresql.commit()
    return postgresql
