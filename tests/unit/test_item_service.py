from datetime import date, timedelta

import pytest

from app import repositories
from app.domain.errors import (
    EstoqueInsuficienteError,
    NaoEncontradoError,
    ValidacaoError,
)
from app.models import Item, Room
from app.services import item_service
from app.services.item_service import resumo_alertas

HOJE = date(2026, 11, 25)


@pytest.fixture
def gerar_resumo(monkeypatch):
    def executar(itens, dias_validade=7, dias_garantia=30):
        monkeypatch.setattr(repositories, "list_items", lambda: itens)

        return resumo_alertas(
            dias_validade=dias_validade, dias_garantia=dias_garantia, hoje=HOJE
        )

    return executar


def test_resumo_sem_itens(gerar_resumo):
    resumo = gerar_resumo([])

    assert resumo["total_itens"] == 0
    assert resumo["vencidos"] == []
    assert resumo["vencendo"] == []
    assert resumo["estoque_baixo"] == []


def test_resumo_identifica_item_vencido(gerar_resumo):
    item = Item(
        nome="Leite", tipo="consumivel", quantidade=1, validade=HOJE - timedelta(days=1)
    )

    resumo = gerar_resumo([item])

    assert resumo["vencidos"] == [item]
    assert resumo["vencendo"] == []


@pytest.mark.parametrize("dias", [0, 7])
def test_resumo_identifica_validade_no_limite(gerar_resumo, dias):
    item = Item(
        nome="Arroz",
        tipo="consumivel",
        quantidade=1,
        validade=HOJE + timedelta(days=dias),
    )

    assert gerar_resumo([item])["vencendo"] == [item]


def test_resumo_ignora_validade_fora_do_prazo(gerar_resumo):
    item = Item(
        nome="Feijao",
        tipo="consumivel",
        quantidade=1,
        validade=HOJE + timedelta(days=8),
    )

    assert gerar_resumo([item])["vencendo"] == []


@pytest.mark.parametrize("quantidade", [0, 1, 2])
def test_resumo_identifica_estoque_baixo(gerar_resumo, quantidade):
    item = Item(
        nome="Sabonete", tipo="consumivel", quantidade=quantidade, estoque_minimo=2
    )

    assert gerar_resumo([item])["estoque_baixo"] == [item]


def test_resumo_ignora_estoque_suficiente(gerar_resumo):
    item = Item(nome="Sabonete", tipo="consumivel", quantidade=3, estoque_minimo=2)

    assert gerar_resumo([item])["estoque_baixo"] == []


def test_resumo_ignora_campos_opcionais_ausentes(gerar_resumo):
    item = Item(nome="Arroz", tipo="consumivel", quantidade=1)

    resumo = gerar_resumo([item])

    assert resumo["vencidos"] == []
    assert resumo["vencendo"] == []
    assert resumo["estoque_baixo"] == []


def test_resumo_contabiliza_itens_por_tipo(gerar_resumo):
    itens = [
        Item(nome="Arroz", tipo="consumivel", quantidade=3),
        Item(nome="Mesa", tipo="duravel", quantidade=1),
    ]

    resumo = gerar_resumo(itens)

    assert resumo["total_itens"] == 2
    assert resumo["total_consumiveis"] == 1
    assert resumo["total_duraveis"] == 1


def test_resumo_identifica_garantia_vencida(gerar_resumo):
    item = Item(
        nome="Geladeira",
        tipo="duravel",
        data_compra=date(2025, 10, 25),
        garantia_meses=12,
    )

    assert gerar_resumo([item])["garantias_vencidas"] == [item]


def test_resumo_identifica_garantia_vencendo(gerar_resumo):
    item = Item(
        nome="Televisao",
        tipo="duravel",
        data_compra=date(2025, 12, 10),
        garantia_meses=12,
    )

    assert gerar_resumo([item])["garantias_vencendo"] == [item]


def test_resumo_ignora_garantia_distante(gerar_resumo):
    item = Item(
        nome="Notebook",
        tipo="duravel",
        data_compra=date(2026, 10, 25),
        garantia_meses=12,
    )

    resumo = gerar_resumo([item])

    assert resumo["garantias_vencendo"] == []
    assert resumo["garantias_vencidas"] == []


def test_resumo_ignora_item_sem_garantia(gerar_resumo):
    item = Item(nome="Mesa", tipo="duravel")

    resumo = gerar_resumo([item])

    assert resumo["garantias_vencendo"] == []
    assert resumo["garantias_vencidas"] == []


def test_resumo_garantia_respeita_prazo_configurado(gerar_resumo):
    item = Item(
        nome="Ventilador",
        tipo="duravel",
        data_compra=date(2025, 12, 10),
        garantia_meses=12,
    )

    resumo = gerar_resumo([item], dias_garantia=7)

    assert resumo["garantias_vencendo"] == []


def test_resumo_garantia_considera_fim_do_mes(monkeypatch):
    item = Item(
        nome="Celular", tipo="duravel", data_compra=date(2026, 1, 31), garantia_meses=1
    )

    monkeypatch.setattr(repositories, "list_items", lambda: [item])

    resumo = resumo_alertas(dias_validade=7, dias_garantia=0, hoje=date(2026, 2, 28))

    assert resumo["garantias_vencendo"] == [item]


def test_resumo_soma_valor_dos_bens_duraveis(gerar_resumo):
    itens = [
        Item(nome="Mesa", tipo="duravel", quantidade=1, valor=500),
        Item(nome="Cadeira", tipo="duravel", quantidade=4, valor=100),
    ]

    resumo = gerar_resumo(itens)

    assert resumo["valor_total_duraveis"] == 900


def test_resumo_nao_soma_valor_de_consumiveis(gerar_resumo):
    item = Item(nome="Arroz", tipo="consumivel", quantidade=2, valor=30)

    assert gerar_resumo([item])["valor_total_duraveis"] == 0


def test_resumo_ignora_duravel_sem_valor(gerar_resumo):
    item = Item(nome="Estante", tipo="duravel", quantidade=1)

    assert gerar_resumo([item])["valor_total_duraveis"] == 0


# ---- criar_item ----
def consumivel(**extras):
    dados = {"nome": "Arroz", "tipo": "consumivel", "quantidade": 2.0}
    dados.update(extras)
    return dados


def duravel(**extras):
    dados = {"nome": "Geladeira", "tipo": "duravel", "quantidade": 1.0}
    dados.update(extras)
    return dados


def test_criar_item_salva_e_devolve_com_id(contexto):
    item = item_service.criar_item(consumivel())
    assert item.id is not None
    assert repositories.get_item(item.id).nome == "Arroz"


def test_criar_item_grava_os_campos_informados(contexto):
    comodo = repositories.add_room(Room(nome="Cozinha"))
    item = item_service.criar_item(
        consumivel(
            categoria="Grãos",
            room_id=comodo.id,
            unidade="kg",
            estoque_minimo=1.0,
            validade=date(2027, 1, 10),
        )
    )
    salvo = repositories.get_item(item.id)
    assert salvo.categoria == "Grãos"
    assert salvo.room.nome == "Cozinha"
    assert salvo.unidade == "kg"
    assert salvo.estoque_minimo == 1.0
    assert salvo.validade == date(2027, 1, 10)


def test_criar_item_sem_comodo_e_aceito(contexto):
    assert item_service.criar_item(consumivel(room_id=None)).room_id is None


def test_criar_item_com_comodo_inexistente_lanca_erro(contexto):
    with pytest.raises(ValidacaoError, match="cômodo escolhido não existe"):
        item_service.criar_item(consumivel(room_id=999))


def test_criar_item_invalido_lanca_erro_e_nao_grava(contexto):
    with pytest.raises(ValidacaoError, match="nome é obrigatório"):
        item_service.criar_item(consumivel(nome=None))
    assert repositories.list_items() == []


def test_criar_consumivel_descarta_campos_de_duravel(contexto):
    item = item_service.criar_item(
        consumivel(
            data_compra=date(2026, 1, 1),
            valor=100.0,
            garantia_meses=12,
        )
    )
    assert (item.data_compra, item.valor, item.garantia_meses) == (None, None, None)


def test_criar_duravel_descarta_campos_de_consumivel(contexto):
    item = item_service.criar_item(
        duravel(
            unidade="un",
            estoque_minimo=1.0,
            validade=date(2027, 1, 1),
        )
    )
    assert (item.unidade, item.estoque_minimo, item.validade) == (None, None, None)


def test_criar_duravel_grava_garantia_e_valor(contexto):
    item = item_service.criar_item(
        duravel(
            data_compra=date(2026, 1, 15),
            valor=3500.0,
            garantia_meses=12,
        )
    )
    assert item.data_compra == date(2026, 1, 15)
    assert item.valor == 3500.0
    assert item.garantia_meses == 12


def test_obter_item_devolve_o_item_cadastrado(contexto):
    criado = item_service.criar_item(consumivel())
    assert item_service.obter_item(criado.id) is criado


def test_obter_item_inexistente_lanca_erro(contexto):
    with pytest.raises(NaoEncontradoError, match="Item não encontrado."):
        item_service.obter_item(999)


def test_editar_item_altera_os_campos_e_grava(contexto):
    item = item_service.criar_item(consumivel())
    item_service.editar_item(item.id, consumivel(nome="Arroz integral", quantidade=5.0))
    salvo = repositories.get_item(item.id)
    assert salvo.nome == "Arroz integral"
    assert salvo.quantidade == 5.0


def test_editar_item_devolve_o_item_alterado(contexto):
    item = item_service.criar_item(consumivel())
    editado = item_service.editar_item(item.id, consumivel(nome="Feijão"))
    assert editado.id == item.id
    assert editado.nome == "Feijão"


def test_editar_item_pode_mudar_o_comodo(contexto):
    comodo = repositories.add_room(Room(nome="Despensa"))
    item = item_service.criar_item(consumivel())
    item_service.editar_item(item.id, consumivel(room_id=comodo.id))
    assert repositories.get_item(item.id).room.nome == "Despensa"


def test_editar_item_mudando_tipo_descarta_campos_do_tipo_antigo(contexto):
    item = item_service.criar_item(consumivel(unidade="kg", validade=date(2027, 1, 1)))
    item_service.editar_item(item.id, duravel(valor=200.0))
    salvo = repositories.get_item(item.id)
    assert salvo.tipo == "duravel"
    assert (salvo.unidade, salvo.validade) == (None, None)
    assert salvo.valor == 200.0


def test_editar_item_invalido_lanca_erro_e_mantem_os_dados(contexto):
    item = item_service.criar_item(consumivel())
    with pytest.raises(ValidacaoError, match="nome é obrigatório"):
        item_service.editar_item(item.id, consumivel(nome="", quantidade=9.0))
    salvo = repositories.get_item(item.id)
    assert salvo.nome == "Arroz"
    assert salvo.quantidade == 2.0


def test_editar_item_inexistente_lanca_erro(contexto):
    with pytest.raises(NaoEncontradoError, match="Item não encontrado."):
        item_service.editar_item(999, consumivel())


def test_remover_item_apaga_o_item(contexto):
    item = item_service.criar_item(consumivel())
    item_service.remover_item(item.id)
    assert repositories.get_item(item.id) is None


def test_remover_item_devolve_o_item_removido(contexto):
    item = item_service.criar_item(consumivel())
    assert item_service.remover_item(item.id).nome == "Arroz"


def test_remover_item_inexistente_lanca_erro(contexto):
    with pytest.raises(NaoEncontradoError, match="Item não encontrado."):
        item_service.remover_item(999)


def test_consumir_item_diminui_a_quantidade_e_grava(contexto):
    item = item_service.criar_item(consumivel(quantidade=5.0))
    item_service.consumir_item(item.id, 2)
    assert repositories.get_item(item.id).quantidade == 3.0


def test_consumir_item_devolve_o_item_atualizado(contexto):
    item = item_service.criar_item(consumivel(quantidade=5.0))
    assert item_service.consumir_item(item.id, 0.5).quantidade == 4.5


def test_consumir_mais_que_o_estoque_lanca_erro_e_mantem_quantidade(contexto):
    item = item_service.criar_item(consumivel(quantidade=2.0))
    with pytest.raises(EstoqueInsuficienteError):
        item_service.consumir_item(item.id, 3)
    assert repositories.get_item(item.id).quantidade == 2.0


def test_consumir_item_duravel_lanca_erro_e_mantem_quantidade(contexto):
    item = item_service.criar_item(duravel(quantidade=1.0))
    with pytest.raises(ValidacaoError, match="Geladeira é durável"):
        item_service.consumir_item(item.id, 1)
    assert repositories.get_item(item.id).quantidade == 1.0


def test_consumir_item_inexistente_lanca_erro(contexto):
    with pytest.raises(NaoEncontradoError):
        item_service.consumir_item(999, 1)


def test_repor_item_aumenta_a_quantidade_e_grava(contexto):
    item = item_service.criar_item(consumivel(quantidade=2.0))
    item_service.repor_item(item.id, 3)
    assert repositories.get_item(item.id).quantidade == 5.0


def test_repor_item_devolve_o_item_atualizado(contexto):
    item = item_service.criar_item(consumivel(quantidade=0.0))
    assert item_service.repor_item(item.id, 1.5).quantidade == 1.5


def test_repor_item_duravel_lanca_erro_e_mantem_quantidade(contexto):
    item = item_service.criar_item(duravel(quantidade=1.0))
    with pytest.raises(ValidacaoError, match="Geladeira é durável"):
        item_service.repor_item(item.id, 1)
    assert repositories.get_item(item.id).quantidade == 1.0


def test_repor_item_inexistente_lanca_erro(contexto):
    with pytest.raises(NaoEncontradoError):
        item_service.repor_item(999, 1)


def listar(**filtros):
    return item_service.listar_itens(hoje=HOJE, **filtros)


def nomes(linhas):
    return [linha["item"].nome for linha in linhas]


def test_listar_itens_sem_cadastro_devolve_lista_vazia(contexto):
    assert listar() == []


def test_listar_itens_vem_em_ordem_alfabetica(contexto):
    item_service.criar_item(consumivel(nome="Sabão"))
    item_service.criar_item(consumivel(nome="Arroz"))
    assert nomes(listar()) == ["Arroz", "Sabão"]


def test_listar_itens_devolve_o_item_com_os_status(contexto):
    item = item_service.criar_item(consumivel())
    assert listar() == [{
        "item": item,
        "validade": "sem_validade",
        "garantia": "sem_garantia",
        "estoque_baixo": False,
    }]


@pytest.mark.parametrize("dias, esperado", [
    (-1, "vencido"),
    (0, "vence_em_breve"),
    (7, "vence_em_breve"),
    (8, "ok"),
])
def test_listar_itens_calcula_status_de_validade(contexto, dias, esperado):
    item_service.criar_item(consumivel(validade=HOJE + timedelta(days=dias)))
    assert listar()[0]["validade"] == esperado


def test_listar_itens_usa_o_prazo_de_validade_informado(contexto):
    item_service.criar_item(consumivel(validade=HOJE + timedelta(days=5)))
    assert item_service.listar_itens(hoje=HOJE, dias_validade=3)[0]["validade"] == "ok"


@pytest.mark.parametrize("data_compra, esperado", [
    (date(2025, 11, 24), "vencida"),
    (date(2025, 12, 10), "vencendo"),
    (date(2026, 10, 25), "em_garantia"),
])
def test_listar_itens_calcula_status_de_garantia(contexto, data_compra, esperado):
    item_service.criar_item(duravel(data_compra=data_compra, garantia_meses=12))
    assert listar()[0]["garantia"] == esperado


def test_listar_itens_usa_o_prazo_de_garantia_informado(contexto):
    item_service.criar_item(duravel(data_compra=date(2025, 12, 10), garantia_meses=12))
    linhas = item_service.listar_itens(hoje=HOJE, dias_garantia=7)
    assert linhas[0]["garantia"] == "em_garantia"


@pytest.mark.parametrize("quantidade, esperado", [(1.0, True), (2.0, True), (3.0, False)])
def test_listar_itens_marca_estoque_baixo(contexto, quantidade, esperado):
    item_service.criar_item(consumivel(quantidade=quantidade, estoque_minimo=2.0))
    assert listar()[0]["estoque_baixo"] is esperado


def test_listar_itens_filtra_por_tipo(contexto):
    item_service.criar_item(consumivel())
    item_service.criar_item(duravel())
    assert nomes(listar(tipo="duravel")) == ["Geladeira"]


def test_listar_itens_filtra_por_comodo(contexto):
    cozinha = repositories.add_room(Room(nome="Cozinha"))
    item_service.criar_item(consumivel(room_id=cozinha.id))
    item_service.criar_item(duravel())
    assert nomes(listar(room_id=cozinha.id)) == ["Arroz"]


def test_listar_itens_busca_parte_do_nome_sem_diferenciar_maiusculas(contexto):
    item_service.criar_item(consumivel(nome="Arroz integral"))
    item_service.criar_item(consumivel(nome="Feijão"))
    assert nomes(listar(busca="INTEGRAL")) == ["Arroz integral"]


@pytest.mark.parametrize("busca", ["", "   ", None])
def test_listar_itens_busca_vazia_nao_filtra(contexto, busca):
    item_service.criar_item(consumivel())
    assert nomes(listar(busca=busca)) == ["Arroz"]


def test_listar_itens_busca_ignora_espacos_nas_pontas(contexto):
    item_service.criar_item(consumivel())
    assert nomes(listar(busca="  arr  ")) == ["Arroz"]


@pytest.fixture
def itens_com_situacoes(contexto):
    item_service.criar_item(consumivel(nome="Leite", validade=HOJE - timedelta(days=1)))
    item_service.criar_item(consumivel(nome="Iogurte", validade=HOJE + timedelta(days=3)))
    item_service.criar_item(consumivel(nome="Sabão", quantidade=1.0, estoque_minimo=2.0))
    item_service.criar_item(duravel(
        nome="Geladeira", data_compra=date(2025, 11, 24), garantia_meses=12,
    ))
    item_service.criar_item(duravel(
        nome="TV", data_compra=date(2025, 12, 10), garantia_meses=12,
    ))
    item_service.criar_item(consumivel(nome="Arroz"))


@pytest.mark.parametrize("situacao, esperado", [
    ("vencido", ["Leite"]),
    ("vence_em_breve", ["Iogurte"]),
    ("estoque_baixo", ["Sabão"]),
    ("garantia_vencida", ["Geladeira"]),
    ("garantia_vencendo", ["TV"]),
])
def test_listar_itens_filtra_por_situacao(itens_com_situacoes, situacao, esperado):
    assert nomes(listar(situacao=situacao)) == esperado


@pytest.mark.parametrize("situacao", [None, "", "desconhecida"])
def test_listar_itens_situacao_vazia_ou_desconhecida_nao_filtra(
    itens_com_situacoes, situacao
):
    assert len(listar(situacao=situacao)) == 6


def test_listar_itens_combina_filtros(contexto):
    cozinha = repositories.add_room(Room(nome="Cozinha"))
    vencido = HOJE - timedelta(days=1)
    item_service.criar_item(consumivel(nome="Leite", room_id=cozinha.id, validade=vencido))
    item_service.criar_item(consumivel(nome="Leite em pó", validade=vencido))
    item_service.criar_item(consumivel(nome="Leite condensado", room_id=cozinha.id))
    assert nomes(listar(room_id=cozinha.id, busca="leite", situacao="vencido")) == ["Leite"]
