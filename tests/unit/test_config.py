from app.config import Config, DevConfig, ProdConfig, TestConfig, url_do_banco


def test_url_do_banco_usa_sqlite_local_quando_nao_ha_variavel(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert url_do_banco() == "sqlite:///casa.db"


def test_url_do_banco_usa_a_variavel_de_ambiente(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///outro.db")
    assert url_do_banco() == "sqlite:///outro.db"


def test_url_do_banco_corrige_prefixo_antigo_do_postgres(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://usuario:senha@host:5432/casa")
    assert url_do_banco() == "postgresql://usuario:senha@host:5432/casa"


def test_url_do_banco_mantem_prefixo_postgresql(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://usuario:senha@host:5432/casa")
    assert url_do_banco() == "postgresql://usuario:senha@host:5432/casa"


def test_config_de_teste_usa_banco_em_memoria():
    assert TestConfig.TESTING is True
    assert TestConfig.SQLALCHEMY_DATABASE_URI == "sqlite://"


def test_config_de_desenvolvimento_ativa_debug():
    assert DevConfig.DEBUG is True


def test_config_de_producao_desativa_debug():
    assert ProdConfig.DEBUG is False


def test_prazos_de_alerta_padrao():
    assert Config.DIAS_ALERTA_VALIDADE == 7
    assert Config.DIAS_ALERTA_GARANTIA == 30
