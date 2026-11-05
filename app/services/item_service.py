# cuida dos itens:

# criar_item(user_id, dados): chama validar_item, depois repositories.add_item
# editar_item, remover_item
# consumir_item(user_id, item_id, qtd): busca o item, chama rules.consumir, salva
# repor_item, mover_item(item_id, novo_room_id)
# listar_itens(user_id, filtros, hoje): devolve os itens já com os status calculados
# registrar_manutencao