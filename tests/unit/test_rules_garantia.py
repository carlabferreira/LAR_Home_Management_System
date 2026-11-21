from datetime import date

import pytest

from app.domain.rules import adicionar_meses, proxima_manutencao, status_garantia

HOJE = date(2026, 11, 4)


def test_adicionar_meses_simples():
    assert adicionar_meses(date(2026, 1, 15), 2) == date(2026, 3, 15)


def test_adicionar_meses_atravessa_o_ano():
    assert adicionar_meses(date(2026, 11, 15), 3) == date(2027, 2, 15)


def test_adicionar_meses_ajusta_para_fim_do_mes_em_ano_comum():
    assert adicionar_meses(date(2026, 1, 31), 1) == date(2026, 2, 28)


def test_adicionar_meses_ajusta_para_fim_do_mes_em_ano_bissexto():
    assert adicionar_meses(date(2028, 1, 31), 1) == date(2028, 2, 29)


def test_adicionar_zero_meses_mantem_a_data():
    assert adicionar_meses(date(2026, 5, 20), 0) == date(2026, 5, 20)


@pytest.mark.parametrize("compra, meses", [(None, 12), (date(2026, 1, 1), 0), (date(2026, 1, 1), None)])
def test_sem_data_ou_sem_meses_nao_ha_garantia(compra, meses):
    assert status_garantia(compra, meses, HOJE) == "sem_garantia"


def test_garantia_longe_do_fim_esta_em_garantia():
    assert status_garantia(date(2026, 1, 1), 12, HOJE) == "em_garantia"


def test_garantia_perto_do_fim_esta_vencendo():
    assert status_garantia(date(2025, 12, 1), 12, HOJE) == "vencendo"


def test_garantia_que_termina_hoje_ainda_esta_vencendo():
    assert status_garantia(date(2025, 11, 4), 12, HOJE) == "vencendo"


def test_garantia_que_terminou_ontem_esta_vencida():
    assert status_garantia(date(2025, 11, 3), 12, HOJE) == "vencida"


def test_prazo_de_alerta_da_garantia_pode_ser_personalizado():
    assert status_garantia(date(2026, 1, 1), 12, HOJE, dias_alerta=90) == "vencendo"


def test_proxima_manutencao_soma_o_intervalo():
    assert proxima_manutencao(date(2026, 8, 10), 6) == date(2027, 2, 10)
