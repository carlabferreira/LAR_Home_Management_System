"""Tabelas do banco. Apenas estrutura de dados, sem regras de negócio."""
from .extensions import db


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    items = db.relationship("Item", back_populates="room")


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # "consumivel" ou "duravel"
    categoria = db.Column(db.String(60))
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    room = db.relationship("Room", back_populates="items")
    quantidade = db.Column(db.Float, nullable=False, default=1)

    # Campos de consumíveis
    unidade = db.Column(db.String(20))
    estoque_minimo = db.Column(db.Float)
    validade = db.Column(db.Date)

    # Campos de bens duráveis
    data_compra = db.Column(db.Date)
    valor = db.Column(db.Float)
    garantia_meses = db.Column(db.Integer)


# Campos que o usuário pode preencher ao criar/editar um item.
CAMPOS_ITEM = (
    "nome", "tipo", "categoria", "room_id", "quantidade",
    "unidade", "estoque_minimo", "validade",
    "data_compra", "valor", "garantia_meses",
)
