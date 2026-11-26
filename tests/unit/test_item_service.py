from datetime import date, timedelta

import pytest

from app import repositories
from app.domain.errors import ValidacaoError
from app.models import Item, Room
from app.services import item_service
from app.services.item_service import resumo_alertas

HOJE = date(2026, 11, 25)


@pytest.fixture
def gerar_resumo(monkeypatch):
    def executar(itens, dias_validade=7, dias_garantia=30):
        monkeypatch.setattr(
            repositories,
            "list_items",
            lambda: itens
        )

        return resumo_alertas(
            dias_validade=dias_validade,
            dias_garantia=dias_garantia,
            hoje=HOJE
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
        nome="Leite",
        tipo="consumivel",
        quantidade=1,
        validade=HOJE - timedelta(days=1)
    )

    resumo = gerar_resumo([item])

    assert resumo["vencidos"] == [item]
    assert resumo["vencendo"] == []


@pytest.mark.parametrize("dias", [0, 7])
def test_resumo_identifica_validade_no_limite(
    gerar_resumo, dias
):
    item = Item(
        nome="Arroz",
        tipo="consumivel",
        quantidade=1,
        validade=HOJE + timedelta(days=dias)
    )

    assert gerar_resumo([item])["vencendo"] == [item]


def test_resumo_ignora_validade_fora_do_prazo(gerar_resumo):
    item = Item(
        nome="Feijao",
        tipo="consumivel",
        quantidade=1,
        validade=HOJE + timedelta(days=8)
    )

    assert gerar_resumo([item])["vencendo"] == []


@pytest.mark.parametrize("quantidade", [0, 1, 2])
def test_resumo_identifica_estoque_baixo(
    gerar_resumo, quantidade
):
    item = Item(
        nome="Sabonete",
        tipo="consumivel",
        quantidade=quantidade,
        estoque_minimo=2
    )

    assert gerar_resumo([item])["estoque_baixo"] == [item]


def test_resumo_ignora_estoque_suficiente(gerar_resumo):
    item = Item(
        nome="Sabonete",
        tipo="consumivel",
        quantidade=3,
        estoque_minimo=2
    )

    assert gerar_resumo([item])["estoque_baixo"] == []


def test_resumo_ignora_campos_opcionais_ausentes(gerar_resumo):
    item = Item(
        nome="Arroz",
        tipo="consumivel",
        quantidade=1
    )

    resumo = gerar_resumo([item])

    assert resumo["vencidos"] == []
    assert resumo["vencendo"] == []
    assert resumo["estoque_baixo"] == []


def test_resumo_contabiliza_itens_por_tipo(gerar_resumo):
    itens = [
        Item(nome="Arroz", tipo="consumivel", quantidade=3),
        Item(nome="Mesa", tipo="duravel", quantidade=1)
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
        garantia_meses=12
    )

    assert gerar_resumo([item])["garantias_vencidas"] == [item]


def test_resumo_identifica_garantia_vencendo(gerar_resumo):
    item = Item(
        nome="Televisao",
        tipo="duravel",
        data_compra=date(2025, 12, 10),
        garantia_meses=12
    )

    assert gerar_resumo([item])["garantias_vencendo"] == [item]


def test_resumo_ignora_garantia_distante(gerar_resumo):
    item = Item(
        nome="Notebook",
        tipo="duravel",
        data_compra=date(2026, 10, 25),
        garantia_meses=12
    )

    resumo = gerar_resumo([item])

    assert resumo["garantias_vencendo"] == []
    assert resumo["garantias_vencidas"] == []


def test_resumo_ignora_item_sem_garantia(gerar_resumo):
    item = Item(
        nome="Mesa",
        tipo="duravel"
    )

    resumo = gerar_resumo([item])

    assert resumo["garantias_vencendo"] == []
    assert resumo["garantias_vencidas"] == []


def test_resumo_garantia_respeita_prazo_configurado(
    gerar_resumo
):
    item = Item(
        nome="Ventilador",
        tipo="duravel",
        data_compra=date(2025, 12, 10),
        garantia_meses=12
    )

    resumo = gerar_resumo([item], dias_garantia=7)

    assert resumo["garantias_vencendo"] == []


def test_resumo_garantia_considera_fim_do_mes(monkeypatch):
    item = Item(
        nome="Celular",
        tipo="duravel",
        data_compra=date(2026, 1, 31),
        garantia_meses=1
    )

    monkeypatch.setattr(
        repositories, "list_items", lambda: [item]
    )

    resumo = resumo_alertas(
        dias_validade=7,
        dias_garantia=0,
        hoje=date(2026, 2, 28)
    )

    assert resumo["garantias_vencendo"] == [item]

def test_resumo_soma_valor_dos_bens_duraveis(gerar_resumo):
    itens = [
        Item(
            nome="Mesa",
            tipo="duravel",
            quantidade=1,
            valor=500
        ),
        Item(
            nome="Cadeira",
            tipo="duravel",
            quantidade=4,
            valor=100
        )
    ]

    resumo = gerar_resumo(itens)

    assert resumo["valor_total_duraveis"] == 900


def test_resumo_nao_soma_valor_de_consumiveis(gerar_resumo):
    item = Item(
        nome="Arroz",
        tipo="consumivel",
        quantidade=2,
        valor=30
    )

    assert gerar_resumo([item])["valor_total_duraveis"] == 0


def test_resumo_ignora_duravel_sem_valor(gerar_resumo):
    item = Item(
        nome="Estante",
        tipo="duravel",
        quantidade=1
    )

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
    item = item_service.criar_item(consumivel(
        categoria="Grãos", room_id=comodo.id, unidade="kg",
        estoque_minimo=1.0, validade=date(2027, 1, 10),
    ))
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
    item = item_service.criar_item(consumivel(
        data_compra=date(2026, 1, 1), valor=100.0, garantia_meses=12,
    ))
    assert (item.data_compra, item.valor, item.garantia_meses) == (None, None, None)


def test_criar_duravel_descarta_campos_de_consumivel(contexto):
    item = item_service.criar_item(duravel(
        unidade="un", estoque_minimo=1.0, validade=date(2027, 1, 1),
    ))
    assert (item.unidade, item.estoque_minimo, item.validade) == (None, None, None)


def test_criar_duravel_grava_garantia_e_valor(contexto):
    item = item_service.criar_item(duravel(
        data_compra=date(2026, 1, 15), valor=3500.0, garantia_meses=12,
    ))
    assert item.data_compra == date(2026, 1, 15)
    assert item.valor == 3500.0
    assert item.garantia_meses == 12
