"""Casos de uso de cômodos. Valida os dados e usa os repositórios para persistir."""
from .. import repositories
from ..domain.errors import ComodoNaoVazioError, NaoEncontradoError, ValidacaoError
from ..models import Room

TAMANHO_MAXIMO_NOME = 80  # mesmo limite da coluna Room.nome


def criar_comodo(nome):
    """Cria um cômodo. O nome é obrigatório e não pode repetir. Lança ValidacaoError."""
    nome = (nome or "").strip()
    if not nome:
        raise ValidacaoError("O nome do cômodo é obrigatório.")
    if len(nome) > TAMANHO_MAXIMO_NOME:
        raise ValidacaoError(
            f"O nome do cômodo deve ter no máximo {TAMANHO_MAXIMO_NOME} caracteres."
        )
    if repositories.get_room_by_nome(nome) is not None:
        raise ValidacaoError(f"Já existe um cômodo com o nome {nome}.")
    return repositories.add_room(Room(nome=nome))


def listar_comodos():
    """Todos os cômodos, em ordem alfabética."""
    return repositories.list_rooms()


def remover_comodo(room_id):
    """Remove um cômodo vazio e o devolve. Recusa cômodo inexistente ou com itens."""
    comodo = repositories.get_room(room_id)
    if comodo is None:
        raise NaoEncontradoError("Cômodo não encontrado.")
    quantidade = repositories.count_items_in_room(room_id)
    if quantidade:
        palavra = "item" if quantidade == 1 else "itens"
        raise ComodoNaoVazioError(
            f"O cômodo {comodo.nome} ainda tem {quantidade} {palavra}. "
            "Remova ou mova os itens antes de excluí-lo."
        )
    repositories.delete_room(comodo)
    return comodo
