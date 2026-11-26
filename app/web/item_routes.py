"""Rotas de itens. Só traduzem HTTP para os serviços; sem regra de negócio."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from ..domain.errors import DominioError
from ..services import item_service, room_service
from .forms import dados_item_do_formulario, mensagens_de_erro

item_bp = Blueprint("items", __name__, url_prefix="/itens")

VALORES_ITEM_NOVO = {"tipo": "consumivel", "quantidade": "1"}


def _avisar_erro(erro):
    for mensagem in mensagens_de_erro(erro):
        flash(mensagem, "erro")


def _formulario(titulo, acao, valores, status=200):
    pagina = render_template(
        "items/form.html",
        titulo=titulo,
        acao=acao,
        valores=valores,
        comodos=room_service.listar_comodos(),
    )
    return pagina, status


@item_bp.get("")
def listar():
    linhas = item_service.listar_itens(
        dias_validade=current_app.config["DIAS_ALERTA_VALIDADE"],
        dias_garantia=current_app.config["DIAS_ALERTA_GARANTIA"],
    )
    return render_template("items/list.html", linhas=linhas)


@item_bp.get("/novo")
def novo():
    return _formulario("Novo item", url_for("items.criar"), VALORES_ITEM_NOVO)


@item_bp.post("/novo")
def criar():
    try:
        item = item_service.criar_item(dados_item_do_formulario(request.form))
    except DominioError as erro:
        _avisar_erro(erro)
        return _formulario("Novo item", url_for("items.criar"), request.form, 400)
    flash(f"Item {item.nome} criado.", "sucesso")
    return redirect(url_for("items.listar"))
