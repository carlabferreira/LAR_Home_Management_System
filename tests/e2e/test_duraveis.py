from datetime import date

import pytest
from playwright.sync_api import expect


pytestmark = pytest.mark.e2e


def test_usuario_cadastra_duravel_com_garantia(
    page, servidor
):
    compra = date.today().isoformat()

    page.goto(f"{servidor}/itens/novo")

    page.locator("#nome").fill("Geladeira")

    page.locator(
        'input[name="tipo"][value="duravel"]'
    ).check()

    page.locator("#quantidade").fill("1")
    page.locator("#valor").fill("2500")
    page.locator("#data_compra").fill(compra)
    page.locator("#garantia_meses").fill("12")

    page.get_by_role(
        "button", name="Salvar"
    ).click()

    expect(page).to_have_url(f"{servidor}/itens")

    linha = page.locator("tbody tr").filter(
        has=page.get_by_role(
            "cell", name="Geladeira", exact=True
        )
    )

    expect(linha).to_be_visible()
    expect(linha.get_by_text("Em garantia")).to_be_visible()

    linha.get_by_role(
        "link", name="Editar"
    ).click()

    expect(
        page.locator("#garantia_meses")
    ).to_have_value("12")

    expect(
        page.locator("#data_compra")
    ).to_have_value(compra)