from datetime import date, timedelta

from app import repositories
from app.models import Item


def test_painel_retorna_status_200(client):
    resposta = client.get("/")

    assert resposta.status_code == 200


def test_painel_exibe_titulo(client):
    resposta = client.get("/")

    assert "Painel da casa" in resposta.get_data(as_text=True)


def test_painel_exibe_totais(client):
    resposta = client.get("/")
    html = resposta.get_data(as_text=True)

    assert "Total de itens" in html
    assert "Consumíveis" in html
    assert "Bens duráveis" in html


def test_painel_exibe_valor_dos_duraveis(client, contexto):
    repositories.add_item(
        Item(
            nome="Mesa",
            tipo="duravel",
            quantidade=1,
            valor=1234.50
        )
    )

    resposta = client.get("/")

    assert "1234.50" in resposta.get_data(as_text=True)

def test_painel_sem_alertas(client):
    resposta = client.get("/")

    assert "Nenhum alerta." in resposta.get_data(as_text=True)


def test_painel_exibe_item_vencido(client, contexto):
    repositories.add_item(
        Item(
            nome="Leite vencido",
            tipo="consumivel",
            quantidade=1,
            validade=date.today() - timedelta(days=1)
        )
    )

    resposta = client.get("/")
    html = resposta.get_data(as_text=True)

    assert "Leite vencido" in html


def test_painel_exibe_item_com_estoque_baixo(client, contexto):
    repositories.add_item(
        Item(
            nome="Sabonete",
            tipo="consumivel",
            quantidade=1,
            estoque_minimo=3
        )
    )

    resposta = client.get("/")

    assert "Sabonete" in resposta.get_data(as_text=True)


def test_painel_exibe_garantia_vencida(client, contexto):
    repositories.add_item(
        Item(
            nome="Geladeira antiga",
            tipo="duravel",
            quantidade=1,
            data_compra=date(2020, 1, 1),
            garantia_meses=12
        )
    )

    resposta = client.get("/")

    assert "Geladeira antiga" in resposta.get_data(as_text=True)


def test_painel_respeita_configuracao_de_validade(
    app, client, contexto
):
    app.config["DIAS_ALERTA_VALIDADE"] = 3

    repositories.add_item(
        Item(
            nome="Produto dentro do prazo",
            tipo="consumivel",
            quantidade=1,
            validade=date.today() + timedelta(days=5)
        )
    )

    resposta = client.get("/")

    assert "Produto dentro do prazo" not in resposta.get_data(
        as_text=True
    )


def test_painel_exibe_item_dentro_do_prazo_configurado(
    app, client, contexto
):
    app.config["DIAS_ALERTA_VALIDADE"] = 10

    repositories.add_item(
        Item(
            nome="Produto proximo do vencimento",
            tipo="consumivel",
            quantidade=1,
            validade=date.today() + timedelta(days=5)
        )
    )

    resposta = client.get("/")

    assert "Produto proximo do vencimento" in resposta.get_data(
        as_text=True
    )


def test_painel_respeita_configuracao_de_garantia(
    app, client, contexto
):
    app.config["DIAS_ALERTA_GARANTIA"] = 0

    repositories.add_item(
        Item(
            nome="Computador",
            tipo="duravel",
            quantidade=1,
            data_compra=date.today(),
            garantia_meses=1
        )
    )

    resposta = client.get("/")

    assert "Computador" not in resposta.get_data(as_text=True)