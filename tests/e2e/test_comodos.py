import pytest
from playwright.sync_api import expect


pytestmark = pytest.mark.e2e


def test_usuario_remove_comodo_vazio(page, servidor):
    page.goto(f"{servidor}/comodos")

    page.get_by_label(
        "Nome do cômodo"
    ).fill("Escritorio")

    page.get_by_role(
        "button", name="Adicionar"
    ).click()

    comodo = page.locator("ul.comodos li").filter(
        has=page.get_by_text(
            "Escritorio", exact=True
        )
    )

    expect(comodo).to_be_visible()

    page.once(
        "dialog",
        lambda dialog: dialog.accept(),
    )

    comodo.get_by_role(
        "button", name="Remover"
    ).click()

    expect(comodo).to_have_count(0)

    expect(
        page.get_by_text(
            "Nenhum cômodo cadastrado ainda."
        )
    ).to_be_visible()