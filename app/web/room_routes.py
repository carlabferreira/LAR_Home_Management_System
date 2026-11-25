"""Rotas de cômodos. Só traduzem HTTP para os serviços; sem regra de negócio."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..domain.errors import DominioError
from ..services import room_service
from .forms import mensagens_de_erro

room_bp = Blueprint("rooms", __name__, url_prefix="/comodos")


def _avisar_erro(erro):
    for mensagem in mensagens_de_erro(erro):
        flash(mensagem, "erro")


@room_bp.get("")
def listar():
    return render_template("rooms/list.html", comodos=room_service.listar_comodos())


@room_bp.post("")
def criar():
    try:
        comodo = room_service.criar_comodo(request.form.get("nome"))
    except DominioError as erro:
        _avisar_erro(erro)
    else:
        flash(f"Cômodo {comodo.nome} criado.", "sucesso")
    return redirect(url_for("rooms.listar"))
