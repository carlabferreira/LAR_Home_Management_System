// Pequenos comportamentos no navegador. As páginas funcionam sem JavaScript;
// este arquivo só melhora a experiência.

const TEMPO_ALERTA_MS = 5000;

// Pede confirmação antes de enviar formulários marcados com data-confirmar.
// Ex.: <form data-confirmar="Remover o cômodo Cozinha?">
document.addEventListener("submit", (evento) => {
  const mensagem = evento.target.dataset.confirmar;
  if (mensagem && !window.confirm(mensagem)) {
    evento.preventDefault();
  }
});

// Esconde sozinhas as mensagens de sucesso; as de erro ficam até a pessoa ler.
function esconderAlerta(alerta) {
  const area = alerta.closest(".alertas");
  const remover = () => {
    alerta.remove();
    if (area && !area.querySelector(".alerta")) {
      area.remove();
    }
  };
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    remover();
    return;
  }
  alerta.addEventListener("transitionend", remover, { once: true });
  alerta.classList.add("sumindo");
}

document.querySelectorAll(".alerta-sucesso").forEach((alerta) => {
  setTimeout(() => esconderAlerta(alerta), TEMPO_ALERTA_MS);
});
