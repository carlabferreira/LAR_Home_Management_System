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


def test_count_items_in_room_conta_so_os_itens_do_comodo(contexto):
    cozinha = repositories.add_room(Room(nome="Cozinha"))
    sala = repositories.add_room(Room(nome="Sala"))
    novo_item("Arroz", room_id=cozinha.id)
    novo_item("Feijão", room_id=cozinha.id)
    novo_item("Sofá", "duravel", room_id=sala.id)
    assert repositories.count_items_in_room(cozinha.id) == 2


def test_count_items_in_room_sem_itens_devolve_zero(contexto):
    comodo = repositories.add_room(Room(nome="Garagem"))
    assert repositories.count_items_in_room(comodo.id) == 0


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


def test_list_items_sem_filtro_vem_em_ordem_de_nome(contexto):
    novo_item("Feijão")
    novo_item("Arroz")
    assert [i.nome for i in repositories.list_items()] == ["Arroz", "Feijão"]


def test_list_items_filtra_por_tipo(contexto):
    novo_item("Arroz")
    novo_item("Geladeira", "duravel")
    assert [i.nome for i in repositories.list_items(tipo="duravel")] == ["Geladeira"]


def test_list_items_filtra_por_comodo(contexto):
    cozinha = repositories.add_room(Room(nome="Cozinha"))
    novo_item("Arroz", room_id=cozinha.id)
    novo_item("Sofá", "duravel")
    assert [i.nome for i in repositories.list_items(room_id=cozinha.id)] == ["Arroz"]


def test_list_items_busca_ignorando_maiusculas(contexto):
    novo_item("Arroz integral")
    novo_item("Feijão")
    assert [i.nome for i in repositories.list_items(busca="ARROZ")] == [
        "Arroz integral"
    ]


def test_list_items_busca_encontra_parte_do_nome(contexto):
    novo_item("Detergente")
    assert [i.nome for i in repositories.list_items(busca="terg")] == ["Detergente"]


def test_list_items_busca_sem_resultado_devolve_lista_vazia(contexto):
    novo_item("Arroz")
    assert repositories.list_items(busca="inexistente") == []


def test_list_items_combina_filtros(contexto):
    cozinha = repositories.add_room(Room(nome="Cozinha"))
    novo_item("Arroz", room_id=cozinha.id)
    novo_item("Fogão", "duravel", room_id=cozinha.id)
    novo_item("Sofá", "duravel")
    nomes = [
        i.nome for i in repositories.list_items(tipo="duravel", room_id=cozinha.id)
    ]
    assert nomes == ["Fogão"]
