from datetime import date

from flask import Flask

from app.web.filters import (
    classe_status, data_br, moeda, numero, register_filters, rotulo_status, rotulo_tipo,
)


def test_data_br_formata_dia_mes_ano():
    assert data_br(date(2026, 3, 5)) == "05/03/2026"


def test_data_br_sem_data_mostra_traco():
    assert data_br(None) == "—"


def test_moeda_usa_formato_brasileiro():
    assert moeda(1234.5) == "R$ 1.234,50"


def test_moeda_de_valor_pequeno_nao_tem_separador_de_milhar():
    assert moeda(7) == "R$ 7,00"


def test_moeda_sem_valor_mostra_traco():
    assert moeda(None) == "—"


def test_numero_remove_zeros_desnecessarios():
    assert numero(5.0) == "5"


def test_numero_mantem_casas_decimais():
    assert numero(2.5) == "2.5"


def test_numero_vazio_ou_none_devolve_texto_vazio():
    assert numero(None) == ""
    assert numero("") == ""


def test_numero_nao_numerico_devolve_o_proprio_texto():
    assert numero("abc") == "abc"


def test_rotulo_de_status_conhecido():
    assert rotulo_status("vence_em_breve") == "Vence em breve"


def test_rotulo_de_status_sem_texto_devolve_vazio():
    assert rotulo_status("sem_validade") == ""


def test_rotulo_de_status_desconhecido_devolve_o_proprio_valor():
    assert rotulo_status("qualquer") == "qualquer"


def test_classe_de_status_conhecido():
    assert classe_status("vencido") == "perigo"
    assert classe_status("vence_em_breve") == "aviso"
    assert classe_status("em_garantia") == "ok"


def test_classe_de_status_desconhecido_devolve_vazio():
    assert classe_status("desconhecido") == ""


def test_rotulo_do_tipo():
    assert rotulo_tipo("consumivel") == "Consumível"
    assert rotulo_tipo("duravel") == "Durável"


def test_register_filters_disponibiliza_os_filtros_no_jinja():
    app = Flask(__name__)
    register_filters(app)
    assert app.jinja_env.filters["data_br"] is data_br
    assert app.jinja_env.filters["moeda"] is moeda
