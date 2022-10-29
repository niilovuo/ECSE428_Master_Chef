import pytest
from app import create_app
from project.db import Db

import os
if os.name == 'nt':
    # if we are on windows, then we want to avoid using pytest-postgresql by
    # providing our own postgresql fixture

    @pytest.fixture
    def postgresql():
        import psycopg2

        pg_user = os.getenv("POSTGRES_USER", "postgres")
        db_args = {
            "password": os.getenv("POSTGRES_PASSWORD"),
            "user": pg_user,
            "dbname": os.getenv("POSTGRES_DB", pg_user),
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": os.getenv("POSTGRES_PORT", 5432)
        }

        # establish connection and destroy all existing data
        conn = psycopg2.connect(**db_args)
        cur = conn.cursor()
        cur.execute(open('./project/destroy.sql').read())
        conn.commit()

        yield conn
        conn.close()

@pytest.fixture
def app(postgresql, monkeypatch):
    app = create_app(setup_db=False)

    monkeypatch.setattr("project.db.Db.init_session", lambda: None)
    monkeypatch.setattr("project.db.Db.deinit_session", lambda: None)
    monkeypatch.setattr("project.db.Db.get_session", lambda: postgresql)

    Db.setup_tables()
    return app

@pytest.fixture
def client(app):
    return app.test_client()
