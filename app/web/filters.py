"""Filtros do Jinja para formatar dados nos templates."""
ROTULOS_STATUS = {
    "ok": "Ok",
    "vencido": "Vencido",
    "vence_em_breve": "Vence em breve",
    "em_garantia": "Em garantia",
    "vencendo": "Garantia vencendo",
    "vencida": "Garantia vencida",
    "sem_validade": "",
    "sem_garantia": "",
}
CLASSES_STATUS = {
    "ok": "ok", "em_garantia": "ok",
    "vence_em_breve": "aviso", "vencendo": "aviso",
    "vencido": "perigo", "vencida": "perigo",
}
ROTULOS_TIPO = {"consumivel": "Consumível", "duravel": "Durável"}


def data_br(data):
    """date(2026, 3, 5) -> '05/03/2026'; None -> '—'."""
    return data.strftime("%d/%m/%Y") if data else "—"


def moeda(valor):
    """1234.5 -> 'R$ 1.234,50'; None -> '—'."""
    if valor is None:
        return "—"
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def numero(valor):
    """5.0 -> '5'; 2.5 -> '2.5'; None ou '' -> ''; texto não numérico fica como está."""
    if valor is None or valor == "":
        return ""
    try:
        return f"{float(valor):g}"
    except (TypeError, ValueError):
        return str(valor)


def rotulo_status(status):
    return ROTULOS_STATUS.get(status, status)


def classe_status(status):
    return CLASSES_STATUS.get(status, "")


def rotulo_tipo(tipo):
    return ROTULOS_TIPO.get(tipo, tipo)


def register_filters(app):
    """Registra todos os filtros acima no Flask (usado pelo create_app)."""
    for funcao in (data_br, moeda, numero, rotulo_status, classe_status, rotulo_tipo):
        app.add_template_filter(funcao, funcao.__name__)
