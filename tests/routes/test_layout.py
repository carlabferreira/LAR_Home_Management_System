import pytest


def html(resposta):
    return resposta.get_data(as_text=True)


def criar_comodo(client, nome):
    return client.post("/comodos", data={"nome": nome}, follow_redirects=True)


# ---- Arquivos estáticos ----
@pytest.mark.parametrize("caminho", [
    "/static/css/style.css",
    "/static/js/main.js",
    "/static/img/logo_branca.png",
    "/static/img/logo_verde.png",
])
def test_arquivos_estaticos_sao_servidos(client, caminho):
    assert client.get(caminho).status_code == 200


# ---- Mensagens (components/_alert.html) ----
def test_mensagem_de_sucesso_usa_estilo_de_sucesso(client):
    assert 'class="alerta alerta-sucesso"' in html(criar_comodo(client, "Cozinha"))


def test_mensagem_de_erro_usa_estilo_de_erro(client):
    assert 'class="alerta alerta-erro"' in html(criar_comodo(client, ""))


def test_mensagem_de_erro_e_anunciada_como_alerta(client):
    assert 'role="alert"' in html(criar_comodo(client, ""))


def test_pagina_sem_mensagens_nao_mostra_area_de_alertas(client):
    assert 'class="alertas"' not in html(client.get("/comodos"))
