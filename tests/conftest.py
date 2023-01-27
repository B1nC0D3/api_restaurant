import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.database import get_session, Base
from main import app

TEST_DB_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres'

engine = create_async_engine(TEST_DB_URL)

TestSession = sessionmaker(engine,
                           class_=AsyncSession,
                           expire_on_commit=False)


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module')
async def test_session():
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        session = TestSession(bind=connection)
        yield session
        await connection.rollback()


@pytest_asyncio.fixture(scope='module')
async def client(test_session):

    def override_get_session():
        try:
            yield test_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url='http://127.0.0.1/api/v1') as client:
        yield client


@pytest_asyncio.fixture(scope='module')
async def create_menu(client):
    data = {
        'title': 'test title',
        'description': 'test desc'
    }
    await client.post('/menus/', json=data)


@pytest_asyncio.fixture(scope='module')
async def create_submenu(client):
    data = {
        'title': 'test title',
        'description': 'test desc'
    }
    await client.post('/menus/1/submenus/', json=data)
