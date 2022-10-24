import pytest
from app import create_app
from project.db import Db

@pytest.fixture
def app(postgresql, monkeypatch):
    app = create_app()
    
    monkeypatch.setattr("project.db.Db.init_session", lambda: None)
    monkeypatch.setattr("project.db.Db.deinit_session", lambda: None)
    monkeypatch.setattr("project.db.Db.get_session", lambda: postgresql)

    Db.setup_tables()
    return app

@pytest.fixture
def client(app):
    return app.test_client()
