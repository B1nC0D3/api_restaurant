import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import get_session
from database.tables import Base
from main import app

TEST_DB_URL = 'sqlite:///tests/test.db'
engine = create_engine(TEST_DB_URL, connect_args={'check_same_thread': False})

TestSession = sessionmaker(engine, autocommit=False, autoflush=False)

Base.metadata.create_all(engine)


@pytest.fixture(scope='module', autouse=True)
def test_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSession(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        session.close()


@pytest.fixture(scope='module', autouse=True)
def client(test_session):

    def override_get_session():
        try:
            yield test_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='module')
def create_menu(client):
    data = {
        'title': 'test title',
        'description': 'test desc'
    }
    client.post('api/v1/menus', json=data)


@pytest.fixture(scope='module')
def create_submenu(client):
    data = {
        'title': 'test title',
        'description': 'test desc'
    }
    client.post('/api/v1/menus/1/submenus', json=data)
