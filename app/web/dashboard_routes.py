# GET /(painel com alertas e totais).

from flask import Blueprint, current_app, render_template

from app.services.item_service import resumo_alertas


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
def index():
    resumo = resumo_alertas(
        dias_validade=current_app.config["DIAS_ALERTA_VALIDADE"],
        dias_garantia=current_app.config["DIAS_ALERTA_GARANTIA"]
    )

    return render_template(
        "dashboard/index.html",
        resumo=resumo
    )