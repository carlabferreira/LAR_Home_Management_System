# é o único lugar que conversa com o banco. Funções como add_item, 
# get_item, list_items(user_id, filtros), update_item, delete_item, 
# get_user_by_email. Nenhum outro arquivo faz db.session.query(...). 
# Se um dia trocar de banco, só este arquivo muda.