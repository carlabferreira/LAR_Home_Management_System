# Home Management System - LAR

# Conteúdo
1. [Integrantes](#1-integrantes)
2. [Sobre o Sistema](#2-sobre-o-sistema)
3. [Tecnologias](#3-tecnologias)
4. [Uso de IA](#4-uso-de-ia)
5. [Execução dos testes](#5-execução-dos-testes)


## 1. Integrantes
- Carla Beatriz Ferreira
- Gabriele Pinheiro Sá
- Laura Oliveira Ribeiro

## 2. Sobre o Sistema

O LAR — Home Management System é uma aplicação web destinada ao gerenciamento e à organização doméstica. O sistema permite controlar os produtos consumíveis e os bens duráveis de uma residência, acompanhar estoques, monitorar prazos de validade e garantias e organizar os itens de acordo com os respectivos cômodos.

O projeto foi desenvolvido utilizando uma arquitetura em camadas, separando as regras de negócio, os serviços, os repositórios, os modelos de dados e a interface web, com o objetivo de facilitar a manutenção e a realização de testes automatizados.

### 2.1 Principais Funcionalidades

* Cadastro, listagem e remoção de cômodos.
* Cadastro, edição, listagem e remoção de itens.
* Controle de estoque de produtos consumíveis.
* Registro de consumo e reposição de produtos.
* Definição de estoque mínimo.
* Controle de validade dos consumíveis.
* Cadastro de bens duráveis e seus respectivos valores.
* Controle de prazos de garantia.
* Filtragem por nome, tipo, cômodo e situação.
* Painel com totais e alertas.
* Cálculo do valor total dos bens duráveis.

### 2.2 Como utilizar o sistema

Clone o repositório:

`git clone https://github.com/carlabferreira/LAR_Home_Management_System.git`

Acesse a pasta:

`cd LAR_Home_Management_System`

Crie um ambiente virtual:

`python -m venv .venv`

Ative o ambiente virtual:

Windows:

`.\.venv\Scripts\Activate.ps1`

Linux/macOS:

`source .venv/bin/activate`

Instale as dependências:

`pip install -r requirements-dev.txt`

Opcionalmente, cadastre dados de exemplo:

`python -m scripts.seed`

Execute a aplicação:

`python -m flask --app app:create_app run --debug`

Acesse http://127.0.0.1:5000

Na página inicial, o usuário pode visualizar os totais e alertas dos itens cadastrados. O menu permite acessar as páginas de cômodos e itens, nas quais é possível cadastrar, consultar, editar e remover registros, conforme as regras de negócio do sistema.

## 3. Tecnologias

* **Python:** linguagem utilizada no desenvolvimento.
* **Flask:** framework responsável pela aplicação web e pelas rotas HTTP.
* **SQLAlchemy:** mapeamento objeto-relacional e persistência dos dados.
* **SQLite:** banco de dados utilizado no desenvolvimento local.
* **PostgreSQL:** banco de dados previsto para produção.
* **HTML, CSS, JavaScript e Jinja2:** construção da interface.
* **Pytest:** implementação e execução dos testes automatizados.
* **Playwright:** execução dos testes end-to-end no navegador.
* **pytest-cov:** geração dos relatórios de cobertura.
* **GitHub Actions:** integração contínua em diferentes sistemas operacionais.
* **Codecov:** acompanhamento da cobertura de testes.
* **Gunicorn:** servidor WSGI para produção.
* **Render:** plataforma escolhida para publicação da aplicação.

## 4. Uso de IA

O Claude e o ChatGPT foram utilizados como ferramentas de apoio ao desenvolvimento de funcionalidades, identificação de erros, organização dos commits e produção da documentação do projeto.

As sugestões produzidas pela ferramenta foram utilizadas como apoio ao desenvolvimento e foram revisadas e validadas mediante a análise do código e a execução dos testes.

## 5. Execução dos testes

1. Prepare o ambiente

```
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\Activate.ps1         # Windows (PowerShell)

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

2. Rode os testes automatizados

| Objetivo | Comando |
| -- | -- |
| Testes de unidade e de rotas (rápido, sem e2e) | ```python -m pytest``` |
| Mais detalhes, um teste por linha	| ```python -m pytest -v``` |
| Só um arquivo | ```python -m pytest tests/unit/test_forms.py``` | 
| Só um teste, pelo nome | ```python -m pytest -k "garantia_vencida"``` |
| Parar no primeiro erro | ```python -m pytest -x ```| 
| Rodar de novo só o que falhou | ```python -m pytest --lf``` |

3. Rode os testes end-to-end

Instale o Chromium:

`python -m playwright install chromium`

Execute os testes:

`python -m pytest -m e2e -v`

Para acompanhar a execução no navegador:

`python -m pytest -m e2e -v --headed`

Os testes end-to-end abrangem cinco fluxos: cadastro de consumível, consumo de produto, cadastro de bem durável com garantia, filtragem de itens e remoção de cômodo.

4. Confira a cobertura

```
python -m pytest --cov=app --cov-report=term-missing
```

5. Rode tudo, como o CI faz
Para os testes e2e, instale o navegador uma vez:

```
python -m playwright install chromium
```

Depois, o mesmo comando do workflow:

```
python -m pytest -v -m "e2e or not e2e" --cov=app --cov-report=term-missing
```

## 6. Links

Repositório: https://github.com/carlabferreira/LAR_Home_Management_System

GitHub Actions: https://github.com/carlabferreira/LAR_Home_Management_System/actions

Aplicação publicada: https://lar-home-management.onrender.com/

Codecov: https://app.codecov.io/gh/carlabferreira/LAR_Home_Management_System

Vídeo demonstrativo: https://youtu.be/dvckLfjVNhY
