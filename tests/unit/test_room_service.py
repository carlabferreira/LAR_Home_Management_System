import pytest

from app import repositories
from app.domain.errors import ComodoNaoVazioError, NaoEncontradoError, ValidacaoError
from app.models import Item
from app.services import room_service


def item_no_comodo(comodo, nome="Arroz"):
    return repositories.add_item(Item(nome=nome, tipo="consumivel", room_id=comodo.id))


# ---- criar_comodo ----
def test_criar_comodo_salva_e_devolve_com_id(contexto):
    comodo = room_service.criar_comodo("Cozinha")
    assert comodo.id is not None
    assert repositories.get_room(comodo.id).nome == "Cozinha"


def test_criar_comodo_remove_espacos_das_pontas(contexto):
    assert room_service.criar_comodo("  Sala  ").nome == "Sala"


@pytest.mark.parametrize("nome", [None, "", "   "])
def test_criar_comodo_sem_nome_lanca_erro(contexto, nome):
    with pytest.raises(ValidacaoError, match="obrigatório"):
        room_service.criar_comodo(nome)


def test_criar_comodo_com_nome_no_limite_e_aceito(contexto):
    assert room_service.criar_comodo("a" * 80).id is not None


def test_criar_comodo_com_nome_longo_demais_lanca_erro(contexto):
    with pytest.raises(ValidacaoError, match="no máximo 80"):
        room_service.criar_comodo("a" * 81)


def test_criar_comodo_com_nome_repetido_lanca_erro(contexto):
    room_service.criar_comodo("Cozinha")
    with pytest.raises(ValidacaoError, match="Já existe"):
        room_service.criar_comodo("Cozinha")


def test_criar_comodo_repetido_com_espacos_tambem_e_recusado(contexto):
    room_service.criar_comodo("Cozinha")
    with pytest.raises(ValidacaoError):
        room_service.criar_comodo(" Cozinha ")


# ---- listar_comodos ----
def test_listar_comodos_sem_cadastro_devolve_lista_vazia(contexto):
    assert room_service.listar_comodos() == []


def test_listar_comodos_vem_em_ordem_alfabetica(contexto):
    room_service.criar_comodo("Sala")
    room_service.criar_comodo("Banheiro")
    assert [c.nome for c in room_service.listar_comodos()] == ["Banheiro", "Sala"]


# ---- remover_comodo ----
def test_remover_comodo_vazio_apaga_o_comodo(contexto):
    comodo = room_service.criar_comodo("Garagem")
    room_service.remover_comodo(comodo.id)
    assert repositories.get_room(comodo.id) is None


def test_remover_comodo_devolve_o_comodo_removido(contexto):
    comodo = room_service.criar_comodo("Garagem")
    assert room_service.remover_comodo(comodo.id).nome == "Garagem"


def test_remover_comodo_com_itens_lanca_erro(contexto):
    comodo = room_service.criar_comodo("Cozinha")
    item_no_comodo(comodo)
    with pytest.raises(ComodoNaoVazioError):
        room_service.remover_comodo(comodo.id)


def test_remover_comodo_com_itens_mantem_o_comodo(contexto):
    comodo = room_service.criar_comodo("Cozinha")
    item_no_comodo(comodo)
    with pytest.raises(ComodoNaoVazioError):
        room_service.remover_comodo(comodo.id)
    assert repositories.get_room(comodo.id) is not None


def test_remover_comodo_com_um_item_usa_singular_na_mensagem(contexto):
    comodo = room_service.criar_comodo("Cozinha")
    item_no_comodo(comodo)
    with pytest.raises(ComodoNaoVazioError, match=r"ainda tem 1 item\."):
        room_service.remover_comodo(comodo.id)


def test_remover_comodo_com_varios_itens_informa_a_quantidade(contexto):
    comodo = room_service.criar_comodo("Cozinha")
    item_no_comodo(comodo, "Arroz")
    item_no_comodo(comodo, "Feijão")
    with pytest.raises(ComodoNaoVazioError, match="ainda tem 2 itens"):
        room_service.remover_comodo(comodo.id)


def test_remover_comodo_inexistente_lanca_erro(contexto):
    with pytest.raises(NaoEncontradoError):
        room_service.remover_comodo(999)
