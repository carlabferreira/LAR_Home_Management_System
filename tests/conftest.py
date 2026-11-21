import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture()
def app():
    """App novo com banco em memória, isolado a cada teste."""
    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def contexto(app):
    """Contexto de aplicação, necessário para testar modelos e repositórios."""
    with app.app_context():
        yield
