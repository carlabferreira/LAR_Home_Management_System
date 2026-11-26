"""Rotas de itens. Só traduzem HTTP para os serviços; sem regra de negócio."""
from flask import Blueprint, current_app, render_template

from ..services import item_service

item_bp = Blueprint("items", __name__, url_prefix="/itens")


@item_bp.get("")
def listar():
    linhas = item_service.listar_itens(
        dias_validade=current_app.config["DIAS_ALERTA_VALIDADE"],
        dias_garantia=current_app.config["DIAS_ALERTA_GARANTIA"],
    )
    return render_template("items/list.html", linhas=linhas)
