# TP: Teste de Software

## Objetivo
Desenvolver e testar um pequeno sistema web, medindo a cobertura de testes, adotando integração e entrega contínuas (CI/CD) e seguindo boas práticas de versionamento.

## Sobre o Sistema

Crie um repositório no GitHub para armazenar o seu sistema. O sistema deve ter um nome próprio e significativo; evite nomes genéricos, como `tp-teste`.

Desenvolva uma pequena aplicação web com funcionalidades básicas que permitam a interação com o usuário. O objetivo principal é demonstrar como os testes contribuem para a manutenção de um sistema de software. A escolha do tema do sistema, da linguagem de programação e das tecnologias é livre.

O repositório deve conter um arquivo `README.md` com as seguintes seções:

- Integrantes: nomes completos dos membros do grupo.
- Sobre o sistema: breve descrição do sistema e de suas funcionalidades.
- Tecnologias: breve explicação sobre as tecnologias utilizadas.
- Uso de IA: detalhes sobre quais ferramentas de IA foram utilizadas e como contribuíram para o desenvolvimento.
- Execução dos testes: instruções para executar os testes localmente.

## Especificação

**Implementar 50 testes de unidade**. Implementar pelo menos 50 testes de unidade. Os testes devem seguir boas práticas, como testes através de API públicas, teste de comportamento, bons nomes, testes focados, testes não-complexos, etc. 

**Implementar 5 end-to-end (e2e)**. Os testes e2e também devem seguir boas práticas, utilizando frameworks como Playwright, Cypress ou Selenium.

**Mensurar cobertura de teste (cobertura ≥ 80%)**. Selecione e utilize alguma ferramenta de cobertura da linguagem escolhida, por exemplo, Coverage.py para Python, Istanbul ou Jest para JavaScript, JaCoCo para Java, etc. A cobertura de testes deve ser ≥ 80%.

**Utilizar CI/CD com GitHub Actions**. Os testes e cobertura devem ser executados automaticamente a cada commit nos sistemas operacionais Linux, MacOS e Windows. Para isso, deve-se configurar e utilizar a ferramenta [GitHub Actions](https://docs.github.com/pt/actions). No GitHub, existem [diversos exemplos](https://docs.github.com/pt/actions/use-cases-and-examples/building-and-testing) sobre como utilizar o GitHub Actions para várias linguagens. *Sugestão*: Configure o GitHub Actions desde o início do desenvolvimento para executar os testes automaticamente desde os primeiros commits.

**Publicar os relatórios de cobertura no Codecov através do GitHub Actions**. O grupo deve utilizar o [Codecov GitHub Action](https://github.com/marketplace/actions/codecov) e fazer o upload do relatório de cobertura no Codecov. Na documentação, você encontra [diversos exemplos](https://docs.codecov.com/docs/supported-languages) sobre como utilizar o Codecov GitHub Action para várias linguagens de programação.

**Utilizar boas práticas de versionamento**. O desenvolvimento deve seguir boas práticas de versionamento, com commits pequenos, frequentes e acompanhados de mensagens descritivas. O projeto deve conter, no mínimo, 50 commits.

**Colocar o sistema em produção**. A aplicação web deve ser publicada em produção por meio de uma plataforma de nuvem com plano gratuito, como Vercel, Netlify, Cloudflare Pages, Render, Fly.io, Firebase Hosting, entre outras.

**Criar um vídeo curto (máximo de 5 minutos).** O vídeo deve apresentar brevemente: (1) o sistema desenvolvido, (2) as tecnologias utilizadas, (3) como as ferramentas de IA foram empregadas e (4) os testes implementados. O vídeo deve ser publicado no YouTube.

## Sobre o Codecov 

Codecov é uma plataforma para publicação online de relatórios de cobertura. Você deve criar uma conta no Codecov e permitir acesso ao GitHub. Exemplos de relatórios de cobertura publicados no Codecov:
VueJS: https://codecov.io/github/vuejs/vue
Django Rest: https://codecov.io/github/encode/django-rest-framework

## Submissão

A entrega deve ser feita pelo Moodle, com os cinco links a seguir:

- Sistema em produção: endereço público da aplicação publicada, em funcionamento.
- Repositório no GitHub: link do repositório com o código-fonte do projeto.
- Build no GitHub Actions: link da execução mais recente concluída com sucesso, mostrando os testes sendo executados (exemplo: https://github.com/Textualize/rich/actions/runs/17610757833).
- Relatório no Codecov: link da página de cobertura de testes do projeto (exemplo: https://codecov.io/github/encode/django-rest-framework).
- Vídeo no YouTube: link do vídeo de apresentação do sistema.
