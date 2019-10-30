import pytest


from fwas import create_app
from fwas.config import TestConfig
from fwas.database import db as _db


@pytest.fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    with _app.app_context():
        # TODO (lmalott): only drop db on each session
        _db.drop_all()
        _db.create_all()

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture()
def client(app):
    yield app.test_client()
