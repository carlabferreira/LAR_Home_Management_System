# cuida dos itens:

# criar_item(user_id, dados): chama validar_item, depois repositories.add_item
# editar_item, remover_item
# consumir_item(user_id, item_id, qtd): busca o item, chama rules.consumir, salva
# repor_item, mover_item(item_id, novo_room_id)
# listar_itens(user_id, filtros, hoje): devolve os itens já com os status calculados
# registrar_manutencao

from datetime import date, timedelta
from decimal import Decimal
from calendar import monthrange

from app import repositories


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

    return resumo