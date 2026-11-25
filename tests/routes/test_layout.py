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
    "/static/img/logo_marca.png",
    "/static/img/apple-touch-icon.png",
    "/static/favicon.ico",
])
def test_arquivos_estaticos_sao_servidos(client, caminho):
    assert client.get(caminho).status_code == 200


@pytest.mark.parametrize("classe", ["alerta-sucesso", "alerta-erro", "botao-perigo"])
def test_css_define_as_classes_usadas_nos_templates(client, classe):
    assert f".{classe}" in client.get("/static/css/style.css").get_data(as_text=True)


# ---- Layout (base.html) ----
def test_layout_carrega_css_e_javascript(client):
    pagina = html(client.get("/comodos"))
    assert "/static/css/style.css" in pagina
    assert "/static/js/main.js" in pagina


def test_layout_define_favicon(client):
    assert 'rel="icon" href="/static/favicon.ico"' in html(client.get("/comodos"))


def test_layout_mostra_logo_com_texto_alternativo(client):
    assert 'alt="LAR · Home Management System"' in html(client.get("/comodos"))


def test_menu_tem_link_para_comodos(client):
    assert 'href="/comodos"' in html(client.get("/comodos"))


def test_menu_destaca_a_pagina_atual(client):
    assert 'aria-current="page"' in html(client.get("/comodos"))


def test_titulo_da_pagina_inclui_o_nome_do_sistema(client):
    assert "<title>Cômodos · LAR</title>" in html(client.get("/comodos"))


# ---- Mensagens (components/_alert.html) ----
def test_mensagem_de_sucesso_usa_estilo_de_sucesso(client):
    assert 'class="alerta alerta-sucesso"' in html(criar_comodo(client, "Cozinha"))


def test_mensagem_de_erro_usa_estilo_de_erro(client):
    assert 'class="alerta alerta-erro"' in html(criar_comodo(client, ""))


def test_mensagem_de_erro_e_anunciada_como_alerta(client):
    assert 'role="alert"' in html(criar_comodo(client, ""))


def test_pagina_sem_mensagens_nao_mostra_area_de_alertas(client):
    assert 'class="alertas"' not in html(client.get("/comodos"))


# ---- Página 404 ----
def test_endereco_inexistente_responde_404(client):
    assert client.get("/endereco-que-nao-existe").status_code == 404


def test_pagina_404_explica_o_problema(client):
    assert "Página não encontrada" in html(client.get("/endereco-que-nao-existe"))


def test_pagina_404_usa_o_layout_do_sistema(client):
    pagina = html(client.get("/endereco-que-nao-existe"))
    assert "/static/css/style.css" in pagina
    assert 'aria-label="Menu principal"' in pagina


def test_pagina_404_tem_link_para_voltar(client):
    assert 'class="botao" href="/comodos"' in html(client.get("/endereco-que-nao-existe"))
