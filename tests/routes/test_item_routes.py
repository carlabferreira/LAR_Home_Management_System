import re

from app import repositories
from app.models import Item, Room


def html(resposta):
    return resposta.get_data(as_text=True)


def cadastrar(app, **campos):
    """Cria um item direto no banco, sem passar pela rota."""
    dados = {"nome": "Arroz", "tipo": "consumivel", "quantidade": 2.0}
    dados.update(campos)
    with app.app_context():
        return repositories.add_item(Item(**dados)).id


# ---- GET /itens ----
def test_pagina_de_itens_responde_com_sucesso(client):
    assert client.get("/itens").status_code == 200


def test_pagina_de_itens_sem_cadastro_mostra_aviso(client):
    assert "Nenhum item cadastrado" in html(client.get("/itens"))


def test_pagina_de_itens_lista_os_cadastrados(app, client):
    cadastrar(app, nome="Arroz")
    cadastrar(app, nome="Geladeira", tipo="duravel")
    pagina = html(client.get("/itens"))
    assert "Arroz" in pagina
    assert "Geladeira" in pagina
    assert "Nenhum item cadastrado" not in pagina


def test_pagina_de_itens_mostra_o_tipo_por_extenso(app, client):
    cadastrar(app, tipo="duravel")
    assert "Durável" in html(client.get("/itens"))


def test_pagina_de_itens_mostra_o_comodo(app, client):
    with app.app_context():
        room_id = repositories.add_room(Room(nome="Despensa")).id
    cadastrar(app, room_id=room_id)
    assert "Despensa" in html(client.get("/itens"))


def test_pagina_de_itens_mostra_quantidade_formatada_com_unidade(app, client):
    cadastrar(app, quantidade=2.0, unidade="kg")
    assert "<td>2 kg</td>" in html(client.get("/itens"))


def test_menu_tem_link_para_itens(client):
    assert 'href="/itens"' in html(client.get("/comodos"))


def test_menu_destaca_itens_na_pagina_de_itens(client):
    assert re.search(r'href="/itens"\s+class="ativo"', html(client.get("/itens")))


def test_menu_nao_destaca_itens_em_outra_pagina(client):
    assert not re.search(r'href="/itens"\s+class="ativo"', html(client.get("/comodos")))
