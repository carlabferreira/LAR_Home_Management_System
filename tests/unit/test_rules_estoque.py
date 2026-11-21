import pytest

from app.domain.errors import EstoqueInsuficienteError, ValidacaoError
from app.domain.rules import abaixo_do_minimo, consumir, repor


def test_consumir_reduz_a_quantidade():
    assert consumir(10, 3) == 7


def test_consumir_tudo_zera_o_estoque():
    assert consumir(5, 5) == 0


def test_consumir_aceita_quantidades_fracionadas():
    assert consumir(2, 0.5) == 1.5


def test_consumir_mais_do_que_existe_lanca_erro():
    with pytest.raises(EstoqueInsuficienteError):
        consumir(2, 3)


@pytest.mark.parametrize("quantidade", [0, -1])
def test_consumir_quantidade_nao_positiva_lanca_erro(quantidade):
    with pytest.raises(ValidacaoError):
        consumir(10, quantidade)


def test_repor_aumenta_a_quantidade():
    assert repor(2, 3) == 5


def test_repor_aceita_quantidades_fracionadas():
    assert repor(1, 0.25) == 1.25


@pytest.mark.parametrize("quantidade", [0, -2])
def test_repor_quantidade_nao_positiva_lanca_erro(quantidade):
    with pytest.raises(ValidacaoError):
        repor(2, quantidade)


def test_abaixo_do_minimo_quando_quantidade_menor():
    assert abaixo_do_minimo(1, 2) is True


def test_abaixo_do_minimo_quando_quantidade_igual_ao_minimo():
    assert abaixo_do_minimo(2, 2) is True


def test_nao_esta_abaixo_do_minimo_quando_quantidade_maior():
    assert abaixo_do_minimo(3, 2) is False


def test_sem_minimo_definido_nunca_esta_abaixo():
    assert abaixo_do_minimo(0, None) is False
