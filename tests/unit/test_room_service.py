import pytest

from app import repositories
from app.domain.errors import ValidacaoError
from app.services import room_service


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
