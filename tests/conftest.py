import pytest
from app import create_app
from config import TestingConfig
from extensions import db as _db
from extensions import STATIC_TOKEN


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers():
    return {'Authorization': f'Bearer {STATIC_TOKEN}'}


@pytest.fixture
def bad_headers():
    return {'Authorization': 'Bearer token-invalido'}
