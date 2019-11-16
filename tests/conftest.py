import pytest
from freezegun import freeze_time

from fwas import create_app
from fwas.config import TestConfig
from fwas.database import db as _db


@pytest.fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    with _app.app_context():
        _db.create_all()
        yield _app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture
def freezer(scope='function', auto_use=True):
    with freeze_time("2019-10-31 12:00:01") as initial:
        yield initial
