# define as tabelas do banco de dados
# Só estrutura de dados, sem regras complexas

# User: id, nome, e-mail, senha_hash
# Room: id, nome, user_id
# Item: id, nome, tipo (consumível ou durável), categoria, room_id, user_id
# campos de consumível: quantidade, unidade, estoque mínimo, validade
# campos de durável: data de compra, valor, meses de garantia
# Maintenance: id, item_id, data, descrição, custo