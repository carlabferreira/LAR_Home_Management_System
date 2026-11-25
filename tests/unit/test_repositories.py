import pytest

from app import repositories
from app.models import Item, Room


def novo_item(nome="Arroz", tipo="consumivel", **extras):
    return repositories.add_item(Item(nome=nome, tipo=tipo, **extras))


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


# ---- Itens ----
def test_add_item_devolve_o_item_com_id(contexto):
    assert novo_item().id is not None


def test_get_item_encontra_item_existente(contexto):
    item = novo_item("Café")
    assert repositories.get_item(item.id).nome == "Café"


def test_get_item_com_id_inexistente_devolve_none(contexto):
    assert repositories.get_item(999) is None


def test_delete_item_remove_o_item(contexto):
    item = novo_item()
    repositories.delete_item(item)
    assert repositories.get_item(item.id) is None
