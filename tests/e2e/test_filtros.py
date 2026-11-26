import pytest
from playwright.sync_api import expect


pytestmark = pytest.mark.e2e


def cadastrar_item(page, servidor, nome, tipo):
    page.goto(f"{servidor}/itens/novo")

    page.locator("#nome").fill(nome)

    page.locator(
        f'input[name="tipo"][value="{tipo}"]'
    ).check()

    page.locator("#quantidade").fill("1")

    page.get_by_role(
        "button", name="Salvar"
    ).click()

    expect(page).to_have_url(f"{servidor}/itens")


def test_usuario_filtra_itens_por_tipo(page, servidor):
    cadastrar_item(
        page, servidor, "Sabonete", "consumivel"
    )

    cadastrar_item(
        page, servidor, "Mesa", "duravel"
    )

    tabela = page.locator("tbody")

    expect(
        tabela.get_by_role(
            "cell", name="Sabonete", exact=True
        )
    ).to_be_visible()

    expect(
        tabela.get_by_role(
            "cell", name="Mesa", exact=True
        )
    ).to_be_visible()

    page.locator("#tipo").select_option("consumivel")

    page.get_by_role(
        "button", name="Filtrar"
    ).click()

    expect(
        tabela.get_by_role(
            "cell", name="Sabonete", exact=True
        )
    ).to_be_visible()

    expect(
        tabela.get_by_role(
            "cell", name="Mesa", exact=True
        )
    ).to_have_count(0)