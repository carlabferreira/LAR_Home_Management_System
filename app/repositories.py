# é o único lugar que conversa com o banco. Funções como add_item,
# get_item, list_items(user_id, filtros), update_item, delete_item,
# get_user_by_email. Nenhum outro arquivo faz db.session.query(...).
# Se um dia trocar de banco, só este arquivo muda.

"""Único módulo que conversa com o banco. Nenhum outro faz consultas diretas."""

from .extensions import db
from .models import Item, Room


# ---- Cômodos ----
def add_room(room):
    db.session.add(room)
    db.session.commit()
    return room


def get_room(room_id):
    return db.session.get(Room, room_id)


def get_room_by_nome(nome):
    return db.session.execute(db.select(Room).filter_by(nome=nome)).scalar_one_or_none()


def list_rooms():
    return db.session.execute(db.select(Room).order_by(Room.nome)).scalars().all()


def delete_room(room):
    db.session.delete(room)
    db.session.commit()


# ---- Itens ----
def add_item(item):
    db.session.add(item)
    db.session.commit()
    return item


def get_item(item_id):
    return db.session.get(Item, item_id)


def list_items(tipo=None, room_id=None, busca=None):
    """Lista itens por ordem de nome, aplicando só os filtros informados."""
    consulta = db.select(Item).order_by(Item.nome)
    if tipo:
        consulta = consulta.where(Item.tipo == tipo)
    if room_id:
        consulta = consulta.where(Item.room_id == room_id)
    if busca:
        consulta = consulta.where(Item.nome.ilike(f"%{busca}%"))
    return db.session.execute(consulta).scalars().all()


def delete_item(item):
    db.session.delete(item)
    db.session.commit()
