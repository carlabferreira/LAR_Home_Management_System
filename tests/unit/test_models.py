from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import CAMPOS_ITEM, Item, Room


def salvar(objeto):
    db.session.add(objeto)
    db.session.commit()
    return objeto


def test_comodo_salvo_recebe_id_e_pode_ser_consultado(contexto):
    salvar(Room(nome="Cozinha"))
    comodo = db.session.execute(db.select(Room).filter_by(nome="Cozinha")).scalar_one()
    assert comodo.id is not None


def test_nome_de_comodo_duplicado_e_rejeitado(contexto):
    salvar(Room(nome="Sala"))
    with pytest.raises(IntegrityError):
        salvar(Room(nome="Sala"))


def test_comodo_sem_nome_e_rejeitado(contexto):
    with pytest.raises(IntegrityError):
        salvar(Room())


def test_item_sem_quantidade_assume_um(contexto):
    item = salvar(Item(nome="Sofá", tipo="duravel"))
    assert item.quantidade == 1


def test_item_sem_nome_e_rejeitado(contexto):
    with pytest.raises(IntegrityError):
        salvar(Item(tipo="duravel"))


def test_item_sem_tipo_e_rejeitado(contexto):
    with pytest.raises(IntegrityError):
        salvar(Item(nome="Sofá"))


def test_item_e_comodo_ficam_ligados_nos_dois_sentidos(contexto):
    cozinha = salvar(Room(nome="Cozinha"))
    arroz = salvar(Item(nome="Arroz", tipo="consumivel", room_id=cozinha.id))
    assert arroz.room.nome == "Cozinha"
    assert [i.nome for i in cozinha.items] == ["Arroz"]


def test_item_consumivel_guarda_validade_e_estoque_minimo(contexto):
    item = salvar(Item(nome="Leite", tipo="consumivel", unidade="L",
                       estoque_minimo=2.0, validade=date(2026, 12, 31)))
    db.session.expire_all()
    recarregado = db.session.get(Item, item.id)
    assert recarregado.validade == date(2026, 12, 31)
    assert recarregado.estoque_minimo == 2.0


def test_item_duravel_guarda_compra_valor_e_garantia(contexto):
    item = salvar(Item(nome="Geladeira", tipo="duravel", valor=2500.0,
                       data_compra=date(2026, 1, 10), garantia_meses=12))
    db.session.expire_all()
    recarregado = db.session.get(Item, item.id)
    assert recarregado.data_compra == date(2026, 1, 10)
    assert recarregado.garantia_meses == 12


def test_todo_campo_editavel_existe_no_modelo_de_item():
    colunas = {coluna.name for coluna in Item.__table__.columns}
    assert set(CAMPOS_ITEM) <= colunas
