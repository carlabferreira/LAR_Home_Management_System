# popula o banco com dados de exemplo (útil na demonstração e no vídeo)

from datetime import date, timedelta

from app import create_app, repositories
from app.domain.rules import adicionar_meses
from app.services import item_service, room_service


def popular_banco():
    hoje = date.today()

    comodos = {}

    for nome in ["Cozinha", "Banheiro", "Quarto", "Sala"]:
        comodo = repositories.get_room_by_nome(nome)

        if comodo is None:
            comodo = room_service.criar_comodo(nome)

        comodos[nome] = comodo.id

    itens = [
        {
            "nome": "Arroz",
            "tipo": "consumivel",
            "categoria": "Alimentos",
            "room_id": comodos["Cozinha"],
            "quantidade": 5,
            "unidade": "kg",
            "estoque_minimo": 2,
            "validade": hoje + timedelta(days=120),
        },
        {
            "nome": "Leite",
            "tipo": "consumivel",
            "categoria": "Alimentos",
            "room_id": comodos["Cozinha"],
            "quantidade": 2,
            "unidade": "L",
            "validade": hoje - timedelta(days=2),
        },
        {
            "nome": "Iogurte",
            "tipo": "consumivel",
            "categoria": "Alimentos",
            "room_id": comodos["Cozinha"],
            "quantidade": 4,
            "unidade": "un",
            "validade": hoje + timedelta(days=3),
        },
        {
            "nome": "Sabonete",
            "tipo": "consumivel",
            "categoria": "Higiene",
            "room_id": comodos["Banheiro"],
            "quantidade": 1,
            "unidade": "un",
            "estoque_minimo": 3,
        },
        {
            "nome": "Geladeira",
            "tipo": "duravel",
            "categoria": "Eletrodomésticos",
            "room_id": comodos["Cozinha"],
            "quantidade": 1,
            "valor": 2500,
            "data_compra": adicionar_meses(hoje, -24),
            "garantia_meses": 12,
        },
        {
            "nome": "Televisão",
            "tipo": "duravel",
            "categoria": "Eletrônicos",
            "room_id": comodos["Sala"],
            "quantidade": 1,
            "valor": 1800,
            "data_compra": adicionar_meses(hoje, -11),
            "garantia_meses": 12,
        },
        {
            "nome": "Guarda-roupa",
            "tipo": "duravel",
            "categoria": "Móveis",
            "room_id": comodos["Quarto"],
            "quantidade": 1,
            "valor": 900,
        },
    ]

    inseridos = 0

    for dados in itens:
        existentes = repositories.list_items(
            room_id=dados["room_id"],
            busca=dados["nome"],
        )

        existe = any(
            item.nome == dados["nome"]
            for item in existentes
        )

        if not existe:
            item_service.criar_item(dados)
            inseridos += 1

    return inseridos


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        quantidade = popular_banco()

        print(f"{quantidade} itens de exemplo cadastrados.")