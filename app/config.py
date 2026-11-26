"""Configurações por ambiente. Valores sensíveis vêm de variáveis de ambiente."""
import os


def url_do_banco():
    """Lê DATABASE_URL (padrão: SQLite local) e corrige o prefixo antigo do PostgreSQL."""
    url = os.environ.get("DATABASE_URL", "sqlite:///casa.db")
    # Algumas plataformas entregam "postgres://", que o SQLAlchemy não aceita.
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = url_do_banco()
    DIAS_ALERTA_VALIDADE = 7
    DIAS_ALERTA_GARANTIA = 30


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "teste"
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # banco em memória, novo a cada app


class ProdConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
