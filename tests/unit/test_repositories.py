import pytest

from app import repositories
from app.models import Item, Room


# ---- Cômodos ----
def test_add_room_devolve_o_comodo_com_id(contexto):
    assert repositories.add_room(Room(nome="Cozinha")).id is not None


def test_get_room_encontra_comodo_existente(contexto):
    comodo = repositories.add_room(Room(nome="Cozinha"))
    assert repositories.get_room(comodo.id).nome == "Cozinha"


def test_get_room_com_id_inexistente_devolve_none(contexto):
    assert repositories.get_room(999) is None


def test_get_room_by_nome_encontra_comodo(contexto):
    repositories.add_room(Room(nome="Sala"))
    assert repositories.get_room_by_nome("Sala").nome == "Sala"


def test_get_room_by_nome_inexistente_devolve_none(contexto):
    assert repositories.get_room_by_nome("Garagem") is None


def test_list_rooms_vazio_devolve_lista_vazia(contexto):
    assert repositories.list_rooms() == []


def test_list_rooms_vem_em_ordem_alfabetica(contexto):
    repositories.add_room(Room(nome="Sala"))
    repositories.add_room(Room(nome="Banheiro"))
    assert [c.nome for c in repositories.list_rooms()] == ["Banheiro", "Sala"]


def test_delete_room_remove_o_comodo(contexto):
    comodo = repositories.add_room(Room(nome="Garagem"))
    repositories.delete_room(comodo)
    assert repositories.get_room(comodo.id) is None
