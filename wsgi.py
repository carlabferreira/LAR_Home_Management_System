# ponto de entrada de produção (app = create_app(ProdConfig)), 
# usado pelo gunicorn wsgi:app

import os

from app import create_app
from app.config import ProdConfig


def criar_app_producao():
    for variavel in ("SECRET_KEY", "DATABASE_URL"):
        if not os.environ.get(variavel):
            raise RuntimeError(
                f"Variável {variavel} não configurada."
            )

    return create_app(ProdConfig)


app = criar_app_producao()