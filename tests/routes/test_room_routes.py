from app import repositories
from app.models import Item, Room


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


# ---- POST /comodos ----
def criar(client, nome):
    return client.post("/comodos", data={"nome": nome}, follow_redirects=True)


def test_criar_comodo_volta_para_a_listagem(client):
    resposta = client.post("/comodos", data={"nome": "Cozinha"})
    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/comodos"


def test_criar_comodo_mostra_mensagem_de_sucesso(client):
    assert "Cômodo Cozinha criado." in html(criar(client, "Cozinha"))


def test_criar_comodo_aparece_na_listagem(client):
    criar(client, "Cozinha")
    assert "Cozinha" in html(client.get("/comodos"))


def test_criar_comodo_sem_nome_mostra_erro(client):
    pagina = html(criar(client, "   "))
    assert "O nome do cômodo é obrigatório." in pagina
    assert "Nenhum cômodo cadastrado" in pagina


def test_criar_comodo_repetido_mostra_erro(app, client):
    cadastrar(app, "Cozinha")
    assert "Já existe um cômodo com o nome Cozinha." in html(criar(client, "Cozinha"))


def test_mensagem_aparece_so_uma_vez(client):
    criar(client, "Cozinha")
    assert "criado" not in html(client.get("/comodos"))


# ---- POST /comodos/<id>/remover ----
def remover(client, room_id):
    return client.post(f"/comodos/{room_id}/remover", follow_redirects=True)


def test_remover_comodo_vazio_mostra_mensagem_de_sucesso(app, client):
    room_id = cadastrar(app, "Garagem")
    assert "Cômodo Garagem removido." in html(remover(client, room_id))


def test_remover_comodo_vazio_tira_da_listagem(app, client):
    room_id = cadastrar(app, "Garagem")
    remover(client, room_id)
    assert "Nenhum cômodo cadastrado" in html(client.get("/comodos"))


def test_remover_comodo_com_itens_mostra_erro_e_mantem_o_comodo(app, client):
    room_id = cadastrar(app, "Cozinha")
    with app.app_context():
        repositories.add_item(Item(nome="Arroz", tipo="consumivel", room_id=room_id))
    assert "ainda tem 1 item" in html(remover(client, room_id))
    assert "Cozinha" in html(client.get("/comodos"))


def test_remover_comodo_inexistente_mostra_erro(client):
    assert "Cômodo não encontrado." in html(remover(client, 999))


def test_remover_comodo_nao_aceita_get(app, client):
    room_id = cadastrar(app, "Garagem")
    assert client.get(f"/comodos/{room_id}/remover").status_code == 405


def test_botao_remover_pede_confirmacao_com_o_nome_do_comodo(app, client):
    cadastrar(app, "Garagem")
    assert 'data-confirmar="Remover o cômodo Garagem?"' in html(client.get("/comodos"))
