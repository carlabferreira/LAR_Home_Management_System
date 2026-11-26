import pytest
from playwright.sync_api import expect


pytestmark = pytest.mark.e2e


def cadastrar_consumivel(page, servidor, nome):
    page.goto(f"{servidor}/itens")

    page.get_by_role(
        "link", name="Novo item"
    ).click()

    page.locator("#nome").fill(nome)

    page.locator(
        'input[name="tipo"][value="consumivel"]'
    ).check()

    page.locator("#quantidade").fill("5")
    page.locator("#unidade").fill("kg")
    page.locator("#estoque_minimo").fill("2")

    page.get_by_role(
        "button", name="Salvar"
    ).click()

    expect(page).to_have_url(f"{servidor}/itens")


def test_usuario_cadastra_consumivel(page, servidor):
    cadastrar_consumivel(page, servidor, "Arroz")

    linha = page.locator("tbody tr").filter(
        has=page.get_by_role(
            "cell", name="Arroz", exact=True
        )
    )

    expect(linha).to_be_visible()

    expect(
        linha.get_by_role("cell", name="5 kg", exact=True)
    ).to_be_visible()


def test_usuario_consumir_reduz_estoque(page, servidor):
    cadastrar_consumivel(page, servidor, "Feijao")

    linha = page.locator("tbody tr").filter(
        has=page.get_by_role(
            "cell", name="Feijao", exact=True
        )
    )

    linha.get_by_label("Quantidade de Feijao").fill("2")

    linha.get_by_role(
        "button", name="Consumir", exact=True
    ).click()

    expect(
        linha.get_by_role("cell", name="3 kg", exact=True)
    ).to_be_visible()