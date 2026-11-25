"""Fábrica da aplicação: monta o Flask e o banco. Sem regra de negócio."""
from flask import Flask, render_template

from . import models  # noqa: F401  (registra as tabelas para o create_all)
from .config import DevConfig
from .extensions import db
from .web.room_routes import room_bp


def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or DevConfig)

    db.init_app(app)

    # As rotas e os filtros do Jinja serão registrados aqui pelas tarefas da camada web.
    app.register_blueprint(room_bp)
    app.register_error_handler(404, pagina_nao_encontrada)

    with app.app_context():
        db.create_all()

    return app
