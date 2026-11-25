from sqlalchemy import inspect

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Room


def test_create_app_aplica_a_configuracao_recebida():
    app = create_app(TestConfig)
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


def test_create_app_registra_a_extensao_do_banco():
    app = create_app(TestConfig)
    assert "sqlalchemy" in app.extensions


def test_create_app_cria_as_tabelas(app):
    with app.app_context():
        tabelas = inspect(db.engine).get_table_names()
    assert {"rooms", "items"} <= set(tabelas)


def test_apps_diferentes_nao_compartilham_dados():
    primeiro, segundo = create_app(TestConfig), create_app(TestConfig)
    with primeiro.app_context():
        db.session.add(Room(nome="Cozinha"))
        db.session.commit()
    with segundo.app_context():
        assert db.session.execute(db.select(Room)).scalars().all() == []
