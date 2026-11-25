"""Rotas de cômodos. Só traduzem HTTP para os serviços; sem regra de negócio."""
from flask import Blueprint, render_template

from ..services import room_service

room_bp = Blueprint("rooms", __name__, url_prefix="/comodos")


@room_bp.get("")
def listar():
    return render_template("rooms/list.html", comodos=room_service.listar_comodos())
