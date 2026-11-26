import re

import pytest

from app import repositories


@pytest.fixture
def criar_item(client, contexto):
    def criar(nome="Arroz", tipo="consumivel", **campos):
        dados = {
            "nome": nome,
            "tipo": tipo,
            "quantidade": "5",
            **campos,
        }

        resposta = client.post(
            "/itens/novo",
            data=dados,
            follow_redirects=True,
        )

        assert resposta.status_code == 200

        itens = repositories.list_items(busca=nome)

        assert len(itens) == 1

        return itens[0].id

    return criar


def linhas_da_tabela(resposta):
    html = resposta.get_data(as_text=True)

    resultado = re.search(
        r"<tbody>(.*?)</tbody>",
        html,
        re.DOTALL,
    )

    return resultado.group(1) if resultado else ""


# Páginas principais


@pytest.mark.parametrize(
    "rota",
    ["/", "/comodos", "/itens", "/itens/novo"],
)
def test_paginas_principais_retornam_200(client, rota):
    resposta = client.get(rota)

    assert resposta.status_code == 200


def test_pagina_inexistente_retorna_404(client):
    resposta = client.get("/pagina-inexistente")

    assert resposta.status_code == 404
    assert "404" in resposta.get_data(as_text=True)


# Cômodos


def test_criar_comodo_redireciona(client):
    resposta = client.post(
        "/comodos",
        data={"nome": "Cozinha"},
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/comodos"


def test_comodo_criado_aparece_na_listagem(client):
    resposta = client.post(
        "/comodos",
        data={"nome": "Cozinha"},
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert "Cozinha" in resposta.get_data(as_text=True)


def test_criar_comodo_sem_nome(client, contexto):
    resposta = client.post(
        "/comodos",
        data={"nome": ""},
        follow_redirects=True,
    )

    assert "obrigatório" in resposta.get_data(as_text=True)
    assert repositories.list_rooms() == []


def test_criar_comodo_duplicado(client, contexto):
    client.post("/comodos", data={"nome": "Cozinha"})

    resposta = client.post(
        "/comodos",
        data={"nome": "Cozinha"},
        follow_redirects=True,
    )

    assert "Já existe" in resposta.get_data(as_text=True)
    assert len(repositories.list_rooms()) == 1


def test_remover_comodo_vazio(client, contexto):
    client.post("/comodos", data={"nome": "Escritorio"})

    comodo = repositories.get_room_by_nome("Escritorio")

    resposta = client.post(
        f"/comodos/{comodo.id}/remover",
    )

    assert resposta.status_code == 302

    assert repositories.get_room_by_nome(
        "Escritorio"
    ) is None


def test_remover_comodo_inexistente(client):
    resposta = client.post(
        "/comodos/99999/remover",
        follow_redirects=True,
    )

    assert "Cômodo não encontrado" in resposta.get_data(
        as_text=True
    )


def test_remover_comodo_ocupado(
    client, contexto, criar_item
):
    client.post(
        "/comodos",
        data={"nome": "Cozinha"},
    )

    comodo = repositories.get_room_by_nome("Cozinha")

    criar_item(room_id=str(comodo.id))

    resposta = client.post(
        f"/comodos/{comodo.id}/remover",
        follow_redirects=True,
    )

    assert "ainda tem 1 item" in resposta.get_data(
        as_text=True
    )

    assert repositories.get_room_by_nome(
        "Cozinha"
    ) is not None


def test_remover_comodo_nao_permite_get(client):
    resposta = client.get("/comodos/1/remover")

    assert resposta.status_code == 405


# Cadastro de itens


def test_cadastrar_consumivel(client, contexto):
    resposta = client.post(
        "/itens/novo",
        data={
            "nome": "Arroz",
            "tipo": "consumivel",
            "quantidade": "5",
            "unidade": "kg",
        },
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/itens"

    item = repositories.list_items(busca="Arroz")[0]

    assert item.quantidade == 5
    assert item.unidade == "kg"


def test_cadastrar_duravel_com_garantia(
    contexto, criar_item
):
    item_id = criar_item(
        nome="Geladeira",
        tipo="duravel",
        quantidade="1",
        valor="2500",
        data_compra="2026-11-01",
        garantia_meses="12",
    )

    item = repositories.get_item(item_id)

    assert item.valor == 2500
    assert item.garantia_meses == 12


@pytest.mark.parametrize(
    "campos, mensagem",
    [
        ({"nome": ""}, "O nome é obrigatório"),
        (
            {"quantidade": "-2"},
            "A quantidade não pode ser negativa",
        ),
        (
            {"quantidade": "abc"},
            "Quantidade: número inválido",
        ),
        (
            {"tipo": "invalido"},
            "O tipo deve ser consumível ou durável",
        ),
        (
            {"room_id": "99999"},
            "O cômodo escolhido não existe",
        ),
        (
            {"validade": "data-invalida"},
            "Validade: data inválida",
        ),
    ],
)
def test_cadastro_invalido_retorna_400(
    client, contexto, campos, mensagem
):
    dados = {
        "nome": "Arroz",
        "tipo": "consumivel",
        "quantidade": "5",
        **campos,
    }

    resposta = client.post("/itens/novo", data=dados)

    assert resposta.status_code == 400
    assert mensagem in resposta.get_data(as_text=True)
    assert repositories.list_items() == []


# Edição


def test_editar_item(client, contexto, criar_item):
    item_id = criar_item()

    resposta = client.post(
        f"/itens/{item_id}/editar",
        data={
            "nome": "Arroz integral",
            "tipo": "consumivel",
            "quantidade": "8",
        },
    )

    assert resposta.status_code == 302

    item = repositories.get_item(item_id)

    assert item.nome == "Arroz integral"
    assert item.quantidade == 8


@pytest.mark.parametrize("metodo", ["GET", "POST"])
def test_editar_item_inexistente_retorna_404(
    client, metodo
):
    resposta = client.open(
        "/itens/99999/editar",
        method=metodo,
    )

    assert resposta.status_code == 404


def test_edicao_invalida_preserva_item(
    client, contexto, criar_item
):
    item_id = criar_item()

    resposta = client.post(
        f"/itens/{item_id}/editar",
        data={
            "nome": "",
            "tipo": "consumivel",
            "quantidade": "5",
        },
    )

    assert resposta.status_code == 400
    assert repositories.get_item(item_id).nome == "Arroz"


# Consumo e reposição


def test_consumir_item(client, contexto, criar_item):
    item_id = criar_item()

    resposta = client.post(
        f"/itens/{item_id}/consumir",
        data={"quantidade": "2"},
    )

    assert resposta.status_code == 302
    assert repositories.get_item(item_id).quantidade == 3


def test_consumir_acima_do_estoque(
    client, contexto, criar_item
):
    item_id = criar_item()

    resposta = client.post(
        f"/itens/{item_id}/consumir",
        data={"quantidade": "6"},
        follow_redirects=True,
    )

    assert "Estoque insuficiente" in resposta.get_data(
        as_text=True
    )

    assert repositories.get_item(item_id).quantidade == 5


def test_repor_item(client, contexto, criar_item):
    item_id = criar_item()

    resposta = client.post(
        f"/itens/{item_id}/repor",
        data={"quantidade": "3"},
    )

    assert resposta.status_code == 302
    assert repositories.get_item(item_id).quantidade == 8


def test_reposicao_invalida_preserva_estoque(
    client, contexto, criar_item
):
    item_id = criar_item()

    resposta = client.post(
        f"/itens/{item_id}/repor",
        data={"quantidade": "-1"},
        follow_redirects=True,
    )

    assert "maior que zero" in resposta.get_data(
        as_text=True
    )

    assert repositories.get_item(item_id).quantidade == 5


# Remoção


def test_remover_item(client, contexto, criar_item):
    item_id = criar_item()

    resposta = client.post(
        f"/itens/{item_id}/remover",
    )

    assert resposta.status_code == 302
    assert repositories.get_item(item_id) is None


def test_remover_item_inexistente(client):
    resposta = client.post(
        "/itens/99999/remover",
        follow_redirects=True,
    )

    assert "Item não encontrado" in resposta.get_data(
        as_text=True
    )


# Filtros


def test_filtrar_itens_por_tipo(client, criar_item):
    criar_item(nome="Feijao")

    criar_item(
        nome="Televisao",
        tipo="duravel",
        quantidade="1",
    )

    resposta = client.get("/itens?tipo=consumivel")

    assert resposta.status_code == 200

    linhas = linhas_da_tabela(resposta)

    assert "<td>Feijao</td>" in linhas
    assert "<td>Televisao</td>" not in linhas


def test_filtrar_itens_por_nome(client, criar_item):
    criar_item(nome="Arroz integral")
    criar_item(nome="Feijao")

    resposta = client.get("/itens?busca=arroz")

    linhas = linhas_da_tabela(resposta)

    assert "<td>Arroz integral</td>" in linhas
    assert "<td>Feijao</td>" not in linhas


def test_filtrar_itens_por_estoque_baixo(
    client, criar_item
):
    criar_item(
        nome="Sabonete",
        quantidade="1",
        estoque_minimo="2",
    )

    criar_item(
        nome="Detergente",
        quantidade="5",
        estoque_minimo="2",
    )

    resposta = client.get(
        "/itens?situacao=estoque_baixo"
    )

    linhas = linhas_da_tabela(resposta)

    assert "<td>Sabonete</td>" in linhas
    assert "<td>Detergente</td>" not in linhas


def test_filtro_sem_resultados(client):
    resposta = client.get("/itens?busca=inexistente")

    assert "Nenhum item encontrado" in resposta.get_data(
        as_text=True
    )