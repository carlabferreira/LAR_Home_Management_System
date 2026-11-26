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