from datetime import date

import pytest

from app.domain.errors import ValidacaoError
from app.domain.rules import validar_item


def consumivel(**mudancas):
    dados = {"nome": "Arroz", "tipo": "consumivel", "quantidade": 2.0, "estoque_minimo": 1.0}
    dados.update(mudancas)
    return dados


def duravel(**mudancas):
    dados = {"nome": "Geladeira", "tipo": "duravel", "quantidade": 1.0, "valor": 2500.0,
             "data_compra": date(2026, 1, 10), "garantia_meses": 12}
    dados.update(mudancas)
    return dados


def erros_de(dados):
    with pytest.raises(ValidacaoError) as excecao:
        validar_item(dados)
    return excecao.value.erros


def test_consumivel_valido_nao_lanca_erro():
    validar_item(consumivel())


def test_duravel_valido_nao_lanca_erro():
    validar_item(duravel())


def test_nome_vazio_e_rejeitado():
    assert "O nome é obrigatório." in erros_de(consumivel(nome=""))


def test_nome_so_com_espacos_e_rejeitado():
    assert "O nome é obrigatório." in erros_de(consumivel(nome="   "))


def test_nome_ausente_e_rejeitado():
    assert "O nome é obrigatório." in erros_de(consumivel(nome=None))


def test_tipo_invalido_e_rejeitado():
    assert "O tipo deve ser consumível ou durável." in erros_de(consumivel(tipo="outro"))


def test_quantidade_negativa_e_rejeitada():
    assert "A quantidade não pode ser negativa." in erros_de(consumivel(quantidade=-1))


def test_quantidade_ausente_e_rejeitada():
    assert "A quantidade é obrigatória." in erros_de(consumivel(quantidade=None))


def test_quantidade_zero_e_permitida():
    validar_item(consumivel(quantidade=0))


def test_estoque_minimo_negativo_e_rejeitado():
    assert "O estoque mínimo não pode ser negativo." in erros_de(consumivel(estoque_minimo=-1))


def test_estoque_minimo_ausente_e_permitido():
    validar_item(consumivel(estoque_minimo=None))


def test_valor_negativo_de_duravel_e_rejeitado():
    assert "O valor não pode ser negativo." in erros_de(duravel(valor=-10))


def test_garantia_negativa_e_rejeitada():
    assert "A garantia não pode ser negativa." in erros_de(duravel(garantia_meses=-1))


def test_garantia_sem_data_de_compra_e_rejeitada():
    assert "Informe a data de compra para usar a garantia." in erros_de(duravel(data_compra=None))


def test_duravel_sem_garantia_nao_exige_data_de_compra():
    validar_item(duravel(garantia_meses=None, data_compra=None))


def test_regras_de_duravel_nao_valem_para_consumivel():
    validar_item(consumivel(valor=-10, garantia_meses=-1))


def test_varios_erros_sao_acumulados():
    assert len(erros_de(consumivel(nome="", quantidade=-1))) == 2
