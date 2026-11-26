from app import repositories
from app.services.item_service import resumo_alertas
from scripts.seed import popular_banco


def test_seed_cadastra_comodos(contexto):
    popular_banco()

    nomes = {
        comodo.nome
        for comodo in repositories.list_rooms()
    }

    assert nomes == {
        "Cozinha", "Banheiro", "Quarto", "Sala"
    }


def test_seed_cadastra_sete_itens(contexto):
    assert popular_banco() == 7
    assert len(repositories.list_items()) == 7


def test_seed_nao_duplica_registros(contexto):
    popular_banco()

    assert popular_banco() == 0

    assert len(repositories.list_rooms()) == 4
    assert len(repositories.list_items()) == 7


def test_seed_cadastra_consumiveis(contexto):
    popular_banco()

    itens = repositories.list_items(tipo="consumivel")

    assert len(itens) == 4


def test_seed_cadastra_duraveis(contexto):
    popular_banco()

    itens = repositories.list_items(tipo="duravel")

    assert len(itens) == 3


def test_seed_gera_alertas_para_demonstracao(contexto):
    popular_banco()

    resumo = resumo_alertas(
        dias_validade=7,
        dias_garantia=31,
    )

    assert len(resumo["vencidos"]) == 1
    assert len(resumo["vencendo"]) == 1
    assert len(resumo["estoque_baixo"]) == 1
    assert len(resumo["garantias_vencidas"]) == 1
    assert len(resumo["garantias_vencendo"]) == 1


def test_seed_gera_valor_total_dos_duraveis(contexto):
    popular_banco()

    resumo = resumo_alertas(
        dias_validade=7,
        dias_garantia=30,
    )

    assert resumo["valor_total_duraveis"] == 5200