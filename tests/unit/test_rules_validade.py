from datetime import date

from app.domain.rules import status_validade

HOJE = date(2026, 11, 4)


def test_sem_validade_informada_retorna_sem_validade():
    assert status_validade(None, HOJE) == "sem_validade"


def test_validade_no_passado_esta_vencida():
    assert status_validade(date(2026, 11, 3), HOJE) == "vencido"


def test_validade_hoje_ainda_nao_esta_vencida():
    assert status_validade(date(2026, 11, 4), HOJE) == "vence_em_breve"