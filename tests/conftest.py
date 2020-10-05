from unittest import mock

import pytest


@pytest.fixture(scope="session")
def app():
    from app import create_app
    app = create_app()
    return app


@pytest.fixture(scope="session", autouse=True)
def app_context(app):
    ctx = app.app_context()
    ctx.push()
    yield
    ctx.pop()


def create_mock_session():
    return mock.Mock()


@pytest.fixture(scope='function', autouse=True)
def db(app):
    import mongoengine
    mongoengine.connect(host=app.config['MONGO_URI'])
    yield
    mongoengine.disconnect()
