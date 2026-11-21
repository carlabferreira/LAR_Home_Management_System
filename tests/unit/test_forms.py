from datetime import date

import pytest
from werkzeug.datastructures import MultiDict

from app.domain.errors import ValidacaoError
from app.web.forms import dados_item_do_formulario, mensagens_de_erro, quantidade_do_formulario


def formulario(**campos):
    return MultiDict(campos)


def erros_de(**campos):
    with pytest.raises(ValidacaoError) as excecao:
        dados_item_do_formulario(formulario(**campos))
    return excecao.value.erros


def test_campos_em_branco_viram_none():
    dados = dados_item_do_formulario(formulario(nome="Arroz", tipo="consumivel", validade=""))
    assert dados["validade"] is None
    assert dados["categoria"] is None


def test_campos_ausentes_viram_none():
    dados = dados_item_do_formulario(formulario())
    assert all(valor is None for valor in dados.values())


def test_espacos_nas_pontas_do_texto_sao_removidos():
    dados = dados_item_do_formulario(formulario(nome="  Arroz  "))
    assert dados["nome"] == "Arroz"


def test_virgula_decimal_e_aceita_em_numeros():
    dados = dados_item_do_formulario(formulario(quantidade="2,5"))
    assert dados["quantidade"] == 2.5


def test_inteiros_sao_convertidos_para_int():
    dados = dados_item_do_formulario(formulario(room_id="3", garantia_meses="12"))
    assert dados["room_id"] == 3
    assert dados["garantia_meses"] == 12


def test_data_iso_e_convertida():
    dados = dados_item_do_formulario(formulario(validade="2026-12-31"))
    assert dados["validade"] == date(2026, 12, 31)


def test_numero_invalido_gera_mensagem_com_o_nome_do_campo():
    assert "Quantidade: número inválido." in erros_de(quantidade="abc")


def test_valor_infinito_e_rejeitado():
    assert "Quantidade: número inválido." in erros_de(quantidade="inf")


def test_data_em_formato_brasileiro_e_rejeitada():
    assert "Validade: data inválida." in erros_de(validade="31/12/2026")


def test_inteiro_com_virgula_e_rejeitado():
    assert "Garantia: número inválido." in erros_de(garantia_meses="1,5")


def test_varios_campos_invalidos_geram_varias_mensagens():
    assert len(erros_de(quantidade="abc", validade="ontem", valor="x")) == 3


def test_quantidade_do_formulario_devolve_numero():
    assert quantidade_do_formulario(formulario(quantidade="3")) == 3.0


def test_quantidade_do_formulario_aceita_virgula():
    assert quantidade_do_formulario(formulario(quantidade="0,5")) == 0.5


def test_quantidade_do_formulario_vazia_lanca_erro():
    with pytest.raises(ValidacaoError) as excecao:
        quantidade_do_formulario(formulario(quantidade=""))
    assert excecao.value.erros == ["Informe a quantidade."]


def test_quantidade_do_formulario_invalida_lanca_erro():
    with pytest.raises(ValidacaoError):
        quantidade_do_formulario(formulario(quantidade="abc"))


def test_mensagens_de_erro_de_validacao_devolve_a_lista():
    assert mensagens_de_erro(ValidacaoError(["a", "b"])) == ["a", "b"]


def test_mensagens_de_erro_de_outra_excecao_devolve_o_texto():
    assert mensagens_de_erro(RuntimeError("falhou")) == ["falhou"]
