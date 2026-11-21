"""Exceções do domínio. As rotas as convertem em mensagens para o usuário."""


class DominioError(Exception):
    """Base de todos os erros de regra de negócio."""


class ValidacaoError(DominioError):
    """Dados inválidos. Guarda a lista de todas as mensagens de erro."""

    def __init__(self, erros):
        if isinstance(erros, str):
            erros = [erros]
        self.erros = list(erros)
        super().__init__("; ".join(self.erros))


class EstoqueInsuficienteError(DominioError):
    pass


class ComodoNaoVazioError(DominioError):
    pass


class NaoEncontradoError(DominioError):
    pass
