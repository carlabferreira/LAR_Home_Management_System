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

### 2.1 Principais Funcionalidades


### 2.2 Como utilizar o sistema


## 3. Tecnologias


## 4. Uso de IA

## 5. Execução dos testes

1. Prepare o ambiente

```
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\Activate.ps1         # Windows (PowerShell)

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

2. Rode os testes

| Objetivo | Comando |
| -- | -- |
| Testes de unidade e de rotas (rápido, sem e2e) | ```python -m pytest``` |
| Mais detalhes, um teste por linha	| ```python -m pytest -v``` |
| Só um arquivo | ```python -m pytest tests/unit/test_forms.py``` | 
| Só um teste, pelo nome | ```python -m pytest -k "garantia_vencida"``` |
| Parar no primeiro erro | ```python -m pytest -x ```| 
| Rodar de novo só o que falhou | ```python -m pytest --lf``` |

3. Confira a cobertura

```
python -m pytest --cov=app --cov-report=term-missing
```

4. Rode tudo, como o CI faz
Para os testes e2e, instale o navegador uma vez:

```
python -m playwright install chromium
```

Depois, o mesmo comando do workflow:

```
python -m pytest -v -m "e2e or not e2e" --cov=app --cov-report=term-missing
```