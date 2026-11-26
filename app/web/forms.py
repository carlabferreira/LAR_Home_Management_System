"""Converte o texto dos formulários em tipos Python, e vice-versa."""

import math
from datetime import date

from ..domain.errors import ValidacaoError
from ..models import CAMPOS_ITEM


def _texto(valor):
    valor = (valor or "").strip()
    return valor or None


def _numero(valor, rotulo, erros, inteiro=False):
    texto = _texto(valor)
    if texto is None:
        return None
    try:
        if inteiro:
            return int(texto)
        numero = float(texto.replace(",", "."))
        if not math.isfinite(numero):
            raise ValueError
        return numero
    except ValueError:
        erros.append(f"{rotulo}: número inválido.")
        return None


def _data(valor, rotulo, erros):
    texto = _texto(valor)
    if texto is None:
        return None
    try:
        return date.fromisoformat(texto)
    except ValueError:
        erros.append(f"{rotulo}: data inválida.")
        return None


def dados_item_do_formulario(form):
    """Monta o dicionário do item. Lança ValidacaoError com todos os campos inválidos."""
    erros = []
    dados = {
        "nome": _texto(form.get("nome")),
        "tipo": _texto(form.get("tipo")),
        "categoria": _texto(form.get("categoria")),
        "room_id": _numero(form.get("room_id"), "Cômodo", erros, inteiro=True),
        "quantidade": _numero(form.get("quantidade"), "Quantidade", erros),
        "unidade": _texto(form.get("unidade")),
        "estoque_minimo": _numero(form.get("estoque_minimo"), "Estoque mínimo", erros),
        "validade": _data(form.get("validade"), "Validade", erros),
        "data_compra": _data(form.get("data_compra"), "Data de compra", erros),
        "valor": _numero(form.get("valor"), "Valor", erros),
        "garantia_meses": _numero(
            form.get("garantia_meses"), "Garantia", erros, inteiro=True
        ),
    }
    if erros:
        raise ValidacaoError(erros)
    return dados


def _texto_do_campo(valor):
    if valor is None:
        return ""
    if isinstance(valor, date):
        return valor.isoformat()
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def valores_do_item(item):
    return {campo: _texto_do_campo(getattr(item, campo)) for campo in CAMPOS_ITEM}


def quantidade_do_formulario(form):
    """Extrai só a quantidade (usada em consumir e repor)."""
    erros = []
    quantidade = _numero(form.get("quantidade"), "Quantidade", erros)
    if erros or quantidade is None:
        raise ValidacaoError(erros or ["Informe a quantidade."])
    return quantidade


def mensagens_de_erro(erro):
    """Transforma uma exceção em lista de textos para mostrar ao usuário."""
    if isinstance(erro, ValidacaoError):
        return erro.erros
    return [str(erro)]
