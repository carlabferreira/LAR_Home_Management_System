# cuida dos itens:

# criar_item(user_id, dados): chama validar_item, depois repositories.add_item
# editar_item, remover_item
# consumir_item(user_id, item_id, qtd): busca o item, chama rules.consumir, salva
# repor_item, mover_item(item_id, novo_room_id)
# listar_itens(user_id, filtros, hoje): devolve os itens já com os status calculados
# registrar_manutencao

from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal

from app import repositories
from app.domain import rules
from app.domain.errors import NaoEncontradoError, ValidacaoError
from app.models import CAMPOS_ITEM, Item

CAMPOS_SO_CONSUMIVEL = ("unidade", "estoque_minimo", "validade")
CAMPOS_SO_DURAVEL = ("data_compra", "valor", "garantia_meses")


def _preparar_dados(dados):
    erros = []
    try:
        rules.validar_item(dados)
    except ValidacaoError as erro:
        erros.extend(erro.erros)

    room_id = dados.get("room_id")
    if room_id is not None and repositories.get_room(room_id) is None:
        erros.append("O cômodo escolhido não existe.")

    if erros:
        raise ValidacaoError(erros)

    descartar = (
        CAMPOS_SO_DURAVEL
        if dados["tipo"] == rules.TIPO_CONSUMIVEL
        else CAMPOS_SO_CONSUMIVEL
    )
    return {
        campo: None if campo in descartar else dados.get(campo) for campo in CAMPOS_ITEM
    }


def criar_item(dados):
    return repositories.add_item(Item(**_preparar_dados(dados)))


def obter_item(item_id):
    item = repositories.get_item(item_id)
    if item is None:
        raise NaoEncontradoError("Item não encontrado.")
    return item


def _fim_garantia(data_compra, meses):
    ano, mes = divmod(data_compra.year * 12 + data_compra.month - 1 + meses, 12)

    mes += 1
    dia = min(data_compra.day, monthrange(ano, mes)[1])

    return date(ano, mes, dia)


def resumo_alertas(dias_validade, dias_garantia, hoje=None):
    hoje = hoje if hoje is not None else date.today()
    itens = repositories.list_items()

    resumo = {
        "total_itens": len(itens),
        "total_consumiveis": 0,
        "total_duraveis": 0,
        "vencidos": [],
        "vencendo": [],
        "estoque_baixo": [],
        "garantias_vencidas": [],
        "garantias_vencendo": [],
        "valor_total_duraveis": Decimal("0.00"),
    }

    limite_validade = hoje + timedelta(days=dias_validade)

    for item in itens:
        if item.tipo == "consumivel":
            resumo["total_consumiveis"] += 1

            if item.validade is not None:
                if item.validade < hoje:
                    resumo["vencidos"].append(item)

                elif item.validade <= limite_validade:
                    resumo["vencendo"].append(item)

            if (
                item.estoque_minimo is not None
                and item.quantidade <= item.estoque_minimo
            ):
                resumo["estoque_baixo"].append(item)

        elif item.tipo == "duravel":
            resumo["total_duraveis"] += 1

            if item.valor is not None:
                resumo["valor_total_duraveis"] += Decimal(str(item.valor)) * Decimal(
                    str(item.quantidade)
                )

            if (
                item.data_compra is not None
                and item.garantia_meses is not None
                and item.garantia_meses > 0
            ):
                fim = _fim_garantia(item.data_compra, item.garantia_meses)

                limite_garantia = hoje + timedelta(days=dias_garantia)

                if fim < hoje:
                    resumo["garantias_vencidas"].append(item)

                elif fim <= limite_garantia:
                    resumo["garantias_vencendo"].append(item)

    return resumo
