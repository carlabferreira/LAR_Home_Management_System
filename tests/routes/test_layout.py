import pytest


# ---- Arquivos estáticos ----
@pytest.mark.parametrize("caminho", [
    "/static/css/style.css",
    "/static/js/main.js",
    "/static/img/logo_branca.png",
    "/static/img/logo_verde.png",
])
def test_arquivos_estaticos_sao_servidos(client, caminho):
    assert client.get(caminho).status_code == 200
