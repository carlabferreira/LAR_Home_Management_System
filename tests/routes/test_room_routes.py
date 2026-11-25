from app import repositories
from app.models import Room


def html(resposta):
    return resposta.get_data(as_text=True)


def cadastrar(app, nome):
    """Cria um cômodo direto no banco, sem passar pela rota."""
    with app.app_context():
        return repositories.add_room(Room(nome=nome)).id


# ---- GET /comodos ----
def test_pagina_de_comodos_responde_com_sucesso(client):
    assert client.get("/comodos").status_code == 200


def test_pagina_de_comodos_sem_cadastro_mostra_aviso(client):
    assert "Nenhum cômodo cadastrado" in html(client.get("/comodos"))


def test_pagina_de_comodos_lista_os_cadastrados(app, client):
    cadastrar(app, "Cozinha")
    cadastrar(app, "Sala")
    pagina = html(client.get("/comodos"))
    assert "Cozinha" in pagina
    assert "Sala" in pagina
