import re
from datetime import date

import pytest

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
    assert "<td>Durável</td>" in html(client.get("/itens"))


def test_pagina_de_itens_mostra_o_comodo(app, client):
    with app.app_context():
        room_id = repositories.add_room(Room(nome="Despensa")).id
    cadastrar(app, room_id=room_id)
    assert "<td>Despensa</td>" in html(client.get("/itens"))


def test_pagina_de_itens_mostra_quantidade_formatada_com_unidade(app, client):
    cadastrar(app, quantidade=2.0, unidade="kg")
    assert "<td>2 kg</td>" in html(client.get("/itens"))


def test_menu_tem_link_para_itens(client):
    assert 'href="/itens"' in html(client.get("/comodos"))


def test_menu_destaca_itens_na_pagina_de_itens(client):
    assert re.search(r'href="/itens"\s+class="ativo"', html(client.get("/itens")))


def test_menu_nao_destaca_itens_em_outra_pagina(client):
    assert not re.search(r'href="/itens"\s+class="ativo"', html(client.get("/comodos")))


def test_pagina_de_itens_tem_botao_para_novo_item(client):
    assert 'href="/itens/novo"' in html(client.get("/itens"))


@pytest.mark.parametrize("consulta, mostrado, escondido", [
    ("tipo=duravel", "Geladeira", "Leite"),
    ("busca=gela", "Geladeira", "Leite"),
    ("situacao=vencido", "Leite", "Geladeira"),
    ("room_id={cozinha}", "Leite", "Geladeira"),
])
def test_pagina_de_itens_aplica_os_filtros_da_url(app, client, consulta, mostrado, escondido):
    with app.app_context():
        cozinha = repositories.add_room(Room(nome="Cozinha")).id
    cadastrar(app, nome="Leite", room_id=cozinha, validade=date(2000, 1, 1))
    cadastrar(app, nome="Geladeira", tipo="duravel")
    pagina = html(client.get("/itens?" + consulta.format(cozinha=cozinha)))
    assert mostrado in pagina
    assert escondido not in pagina


def test_pagina_de_itens_mantem_os_filtros_escolhidos(app, client):
    with app.app_context():
        cozinha = repositories.add_room(Room(nome="Cozinha")).id
    pagina = html(client.get(
        f"/itens?busca=lei&tipo=consumivel&room_id={cozinha}&situacao=estoque_baixo"
    ))
    assert 'value="lei"' in pagina
    assert 'value="consumivel" selected' in pagina
    assert f'value="{cozinha}" selected' in pagina
    assert 'value="estoque_baixo" selected' in pagina


def test_pagina_de_itens_sem_resultado_no_filtro_mostra_aviso(app, client):
    cadastrar(app)
    pagina = html(client.get("/itens?busca=inexistente"))
    assert "Nenhum item encontrado com esses filtros." in pagina
    assert "Nenhum item cadastrado" not in pagina


def test_pagina_de_itens_mostra_selos_de_situacao(app, client):
    cadastrar(app, nome="Leite", validade=date(2000, 1, 1), quantidade=0.0, estoque_minimo=1.0)
    cadastrar(app, nome="TV", tipo="duravel", data_compra=date.today(), garantia_meses=12)
    pagina = html(client.get("/itens"))
    assert '<span class="etiqueta perigo">Vencido</span>' in pagina
    assert '<span class="etiqueta aviso">Estoque baixo</span>' in pagina
    assert '<span class="etiqueta ok">Em garantia</span>' in pagina


def test_pagina_de_itens_tem_link_para_editar_cada_item(app, client):
    item_id = cadastrar(app)
    assert f'href="/itens/{item_id}/editar"' in html(client.get("/itens"))


# ---- GET /itens/novo ----
def test_formulario_novo_item_envia_para_a_rota_de_criacao(client):
    assert 'action="/itens/novo"' in html(client.get("/itens/novo"))


def test_formulario_novo_item_vem_como_consumivel_com_quantidade_1(client):
    pagina = html(client.get("/itens/novo"))
    assert re.search(r'value="consumivel"\s+checked', pagina)
    assert 'value="1"' in pagina


def test_formulario_novo_item_oferece_os_comodos(app, client):
    with app.app_context():
        repositories.add_room(Room(nome="Despensa"))
    pagina = html(client.get("/itens/novo"))
    assert "Sem cômodo" in pagina
    assert "Despensa" in pagina


# ---- POST /itens/novo ----
def form_item(**campos):
    """Dados como o navegador envia: tudo texto."""
    dados = {"nome": "Arroz", "tipo": "consumivel", "quantidade": "2"}
    dados.update(campos)
    return dados


def criar(client, **campos):
    return client.post("/itens/novo", data=form_item(**campos), follow_redirects=True)


def test_criar_item_volta_para_a_listagem(client):
    resposta = client.post("/itens/novo", data=form_item())
    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/itens"


def test_criar_item_mostra_mensagem_de_sucesso(client):
    assert "Item Arroz criado." in html(criar(client))


def test_criar_item_grava_os_campos_do_formulario(app, client):
    with app.app_context():
        room_id = repositories.add_room(Room(nome="Sala")).id
    criar(
        client,
        nome="TV",
        tipo="duravel",
        quantidade="1",
        room_id=str(room_id),
        data_compra="2026-01-15",
        valor="2500,90",
        garantia_meses="12",
    )
    with app.app_context():
        item = repositories.list_items()[0]
        assert item.room.nome == "Sala"
        assert item.valor == 2500.90
        assert item.garantia_meses == 12


def test_criar_item_invalido_responde_400_e_nao_grava(app, client):
    resposta = client.post("/itens/novo", data=form_item(nome=""))
    assert resposta.status_code == 400
    with app.app_context():
        assert repositories.list_items() == []


def test_criar_item_invalido_mostra_todos_os_erros(client):
    pagina = html(criar(client, nome="", quantidade="-1"))
    assert "O nome é obrigatório." in pagina
    assert "A quantidade não pode ser negativa." in pagina


def test_criar_item_invalido_mantem_o_que_foi_digitado(app, client):
    with app.app_context():
        room_id = repositories.add_room(Room(nome="Despensa")).id
    pagina = html(
        criar(
            client,
            nome="Leite",
            tipo="duravel",
            quantidade="-1",
            categoria="Laticínios",
            room_id=str(room_id),
            data_compra="2026-01-10",
        )
    )
    assert 'value="Leite"' in pagina
    assert 'value="-1"' in pagina
    assert 'value="Laticínios"' in pagina
    assert 'value="2026-01-10"' in pagina
    assert re.search(rf'value="{room_id}"\s+selected', pagina)
    assert re.search(r'value="duravel"\s+checked', pagina)


def test_erro_do_formulario_nao_reaparece_na_proxima_pagina(client):
    criar(client, nome="")
    assert "O nome é obrigatório." not in html(client.get("/itens"))


def test_formulario_editar_vem_preenchido_com_o_item(app, client):
    with app.app_context():
        room_id = repositories.add_room(Room(nome="Despensa")).id
    item_id = cadastrar(
        app,
        nome="Leite",
        quantidade=2.0,
        unidade="L",
        estoque_minimo=1.5,
        room_id=room_id,
        validade=date(2027, 1, 10),
    )
    pagina = html(client.get(f"/itens/{item_id}/editar"))
    assert f'action="/itens/{item_id}/editar"' in pagina
    assert 'value="Leite"' in pagina
    assert 'value="2"' in pagina
    assert 'value="1.5"' in pagina
    assert 'value="2027-01-10"' in pagina
    assert re.search(rf'value="{room_id}"\s+selected', pagina)
    assert re.search(r'value="consumivel"\s+checked', pagina)


def test_formulario_editar_mostra_valor_grande_sem_notacao_cientifica(app, client):
    item_id = cadastrar(app, tipo="duravel", valor=1234567.0)
    assert 'value="1234567"' in html(client.get(f"/itens/{item_id}/editar"))


def editar(client, item_id, **campos):
    return client.post(
        f"/itens/{item_id}/editar", data=form_item(**campos), follow_redirects=True
    )


def test_editar_item_grava_e_volta_para_a_listagem_com_mensagem(app, client):
    item_id = cadastrar(app)
    resposta = editar(client, item_id, nome="Arroz integral", quantidade="5")
    assert resposta.request.path == "/itens"
    assert "Item Arroz integral atualizado." in html(resposta)
    with app.app_context():
        item = repositories.get_item(item_id)
        assert (item.nome, item.quantidade) == ("Arroz integral", 5.0)


def test_editar_item_invalido_mantem_o_digitado_e_nao_altera(app, client):
    item_id = cadastrar(app)
    resposta = editar(client, item_id, nome="", quantidade="9")
    pagina = html(resposta)
    assert resposta.status_code == 400
    assert "O nome é obrigatório." in pagina
    assert 'value="9"' in pagina
    with app.app_context():
        assert repositories.get_item(item_id).quantidade == 2.0


def test_editar_item_inexistente_responde_404(client):
    assert client.post("/itens/999/editar", data=form_item()).status_code == 404
