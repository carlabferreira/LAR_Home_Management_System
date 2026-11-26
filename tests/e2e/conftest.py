from threading import Thread

import pytest
from werkzeug.serving import make_server

from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture
def servidor(tmp_path):
    class E2EConfig(TestConfig):
        SQLALCHEMY_DATABASE_URI = (
            f"sqlite:///{(tmp_path / 'e2e.db').as_posix()}"
        )

    app = create_app(E2EConfig)

    http = make_server("127.0.0.1", 0, app)

    thread = Thread(
        target=http.serve_forever,
        daemon=True,
    )

    thread.start()

    try:
        yield f"http://127.0.0.1:{http.server_port}"
    finally:
        http.shutdown()
        thread.join()
        http.server_close()

        with app.app_context():
            db.session.remove()
            db.engine.dispose()