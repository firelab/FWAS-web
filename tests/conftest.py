import pytest
from freezegun import freeze_time

from fwas.main import get_application
from fwas.database import database


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    # Create test database
    engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)
    engine.execute('create extension if not exists "uuid-ossp"')
    metadata.create_all(engine)

    # Run the test suite
    yield

    # Drop test databases
    metadata.drop_all(engine)


@pytest.fixture
async def db():
    if not database.is_connected:
        await database.connect()
        await init_db()

    yield database

    if database.is_connected:
        await database.disconnect()


@pytest.fixture
async def client():
    application = get_application()

    async with TestClient(application) as client:
        await init_db()
        yield client


@pytest.fixture
def freezer(scope='function', auto_use=True):
    with freeze_time("2019-10-31 12:00:01") as initial:
        yield initial
