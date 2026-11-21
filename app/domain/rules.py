"""Regras de negócio puras: sem Flask, sem banco, sem relógio.

A data de "hoje" é sempre recebida como parâmetro, o que deixa tudo
determinístico e fácil de testar.
"""
import calendar
from datetime import date

from .errors import EstoqueInsuficienteError, ValidacaoError

TIPO_CONSUMIVEL = "consumivel"
TIPO_DURAVEL = "duravel"
TIPOS = (TIPO_CONSUMIVEL, TIPO_DURAVEL)


# ---------------------------------------------------------------------------
# Validade
# ---------------------------------------------------------------------------
def status_validade(validade, hoje, dias_alerta=7):
    """Retorna: sem_validade, vencido, vence_em_breve ou ok."""
    if validade is None:
        return "sem_validade"
    dias_restantes = (validade - hoje).days
    if dias_restantes < 0:
        return "vencido"
    if dias_restantes <= dias_alerta:
        return "vence_em_breve"
    return "ok"


# ---------------------------------------------------------------------------
# Tarefa 1: garantia e datas
# ---------------------------------------------------------------------------
def adicionar_meses(data, meses):
    """Soma meses a uma data, ajustando o dia ao fim do mês quando necessário."""
    indice = data.month - 1 + meses
    ano = data.year + indice // 12
    mes = indice % 12 + 1
    dia = min(data.day, calendar.monthrange(ano, mes)[1])
    return date(ano, mes, dia)


def status_garantia(data_compra, meses, hoje, dias_alerta=30):
    """Retorna: sem_garantia, vencida, vencendo ou em_garantia."""
    if data_compra is None or not meses:
        return "sem_garantia"
    fim = adicionar_meses(data_compra, meses)
    dias_restantes = (fim - hoje).days
    if dias_restantes < 0:
        return "vencida"
    if dias_restantes <= dias_alerta:
        return "vencendo"
    return "em_garantia"


def proxima_manutencao(ultima, intervalo_meses):
    """Data da próxima manutenção, a partir da última e do intervalo em meses."""
    return adicionar_meses(ultima, intervalo_meses)

# ---------------------------------------------------------------------------
# Tarefa 2: estoque
# ---------------------------------------------------------------------------
def consumir(quantidade_atual, quantidade):
    """Devolve a nova quantidade após o consumo."""
    if quantidade <= 0:
        raise ValidacaoError("A quantidade consumida deve ser maior que zero.")
    if quantidade > quantidade_atual:
        raise EstoqueInsuficienteError(
            f"Estoque insuficiente: há {quantidade_atual:g} e foram pedidos {quantidade:g}."
        )
    return round(quantidade_atual - quantidade, 3)


def repor(quantidade_atual, quantidade):
    """Devolve a nova quantidade após a reposição."""
    if quantidade <= 0:
        raise ValidacaoError("A quantidade reposta deve ser maior que zero.")
    return round(quantidade_atual + quantidade, 3)


def abaixo_do_minimo(quantidade, estoque_minimo):
    """Estoque baixo: quantidade menor ou igual ao mínimo definido."""
    if estoque_minimo is None:
        return False
    return quantidade <= estoque_minimo

# ---------------------------------------------------------------------------
# Tarefa 3: validação de item
# ---------------------------------------------------------------------------
def validar_item(dados):
    """Valida os dados (já convertidos para tipos Python). Lança ValidacaoError."""
    erros = []

    if not (dados.get("nome") or "").strip():
        erros.append("O nome é obrigatório.")

    tipo = dados.get("tipo")
    if tipo not in TIPOS:
        erros.append("O tipo deve ser consumível ou durável.")

    quantidade = dados.get("quantidade")
    if quantidade is None:
        erros.append("A quantidade é obrigatória.")
    elif quantidade < 0:
        erros.append("A quantidade não pode ser negativa.")

    if tipo == TIPO_CONSUMIVEL:
        minimo = dados.get("estoque_minimo")
        if minimo is not None and minimo < 0:
            erros.append("O estoque mínimo não pode ser negativo.")

    if tipo == TIPO_DURAVEL:
        valor = dados.get("valor")
        if valor is not None and valor < 0:
            erros.append("O valor não pode ser negativo.")
        garantia = dados.get("garantia_meses")
        if garantia is not None and garantia < 0:
            erros.append("A garantia não pode ser negativa.")
        if garantia and dados.get("data_compra") is None:
            erros.append("Informe a data de compra para usar a garantia.")

    if erros:
        raise ValidacaoError(erros)

