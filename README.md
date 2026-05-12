# Squad QA — Agentes de Automacao de Testes para Claude Code

Squad de agentes de automacao de testes de ambiente integrado ao Claude Code. Recebe casos de teste em Gherkin, passo a passo ou CSV e os executa automaticamente em browsers, APIs, banco de dados, performance, acessibilidade e seguranca — entregando um relatorio HTML consolidado ao final.

## Agentes disponíveis (15)

### Orquestradores

| Agente | Comando | Descricao |
|---|---|---|
| **orquestrador-qa** | `/orquestrador-qa` | Ponto de entrada principal do squad de execucao. Recebe casos de teste, classifica e despacha para os executores em paralelo, gerando relatorio consolidado |
| **qa-pipeline** | `/qa-pipeline` | Orquestra o pipeline de planejamento QA: recebe uma historia de usuario e entrega criterios de aceite + cenarios de teste |

### Executores de teste

| Agente | Comando | Descricao |
|---|---|---|
| **executor-browser** | `/executor-browser` | Executa testes de browser e UI (smoke, sanity, regressao, E2E, cross-browser) usando Playwright + TypeScript + Page Object Model |
| **executor-api** | `/executor-api` | Executa testes de API REST e integracao usando Playwright APIRequestContext com TypeScript. Valida contratos com Zod |
| **executor-performance** | `/executor-performance` | Executa testes de performance, carga, stress e soak usando k6. Retorna metricas de latencia, throughput e taxa de erro |
| **executor-visual** | `/executor-visual` | Executa testes de regressao visual usando Playwright com comparacao de screenshots. Detecta alteracoes visuais nao intencionais |
| **executor-acessibilidade** | `/executor-acessibilidade` | Executa testes de acessibilidade WCAG usando axe-core via Playwright. Detecta violacoes por impacto (critical, serious, moderate, minor) |
| **executor-seguranca** | `/executor-seguranca` | Executa verificacoes basicas de seguranca nao invasivas: autenticacao, headers HTTP, CORS e endpoints sensiveis expostos |
| **executor-banco** | `/executor-banco` | Executa testes de integridade e persistencia de dados no banco de dados. Requer variavel de ambiente `DB_CONNECTION_STRING` |

### Agentes de suporte ao planejamento

| Agente | Comando | Descricao |
|---|---|---|
| **classifier-testes** | `/classifier-testes` | Classifica cada caso de teste por tipo e executor adequado. Retorna clarificacao estruturada quando ha ambiguidade |
| **reporter-qa** | `/reporter-qa` | Consolida resultados de todos os executores e gera relatorio HTML dual-mode (resumo amigavel + tecnico com codigo/logs) |
| **gerador-criterios-aceite** | `/gerador-criterios-aceite` | Gera criterios de aceite, plano de testes e mapa mental a partir de uma historia de usuario |
| **gerador-cenarios-teste** | `/gerador-cenarios-teste` | Gera cenarios de teste em Gherkin, passo a passo ou CSV para Azure DevOps a partir de criterios de aceite |

### Agentes standalone

| Agente | Comando | Descricao |
|---|---|---|
| **consulta-treinamento** | `/consulta-treinamento` | Consulta o progresso de treinamento de colaboradores em planilha Excel, com busca tolerante a erros de digitacao |
| **revisor** | `/revisor` | Revisa textos em portugues brasileiro |

## Pre-requisitos

Antes de instalar, certifique-se de ter:

- **Node.js** >= 18 — [nodejs.org](https://nodejs.org)
- **Python** >= 3.9 — [python.org](https://python.org)
- **k6** — necessario apenas para testes de performance:
  ```powershell
  winget install k6
  ```

## Instalacao

```powershell
# 1. Clone o repositorio
git clone https://github.com/carminitti/Agentes.git
cd Agentes

# 2. Execute o script de instalacao
.\install.ps1

# 3. Reinicie o Claude Code
```

Se o PowerShell bloquear a execucao do script:
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

O script instala os agentes no perfil local do Claude Code via `claude plugin install`. Apos reiniciar o Claude Code, todos os comandos listados acima estarao disponiveis.

## Como usar

### Executar uma suite de testes de ambiente

Abra qualquer sessao do Claude Code e use:

```
/orquestrador-qa

TC-001: Login com credenciais validas
  Dado que acesso https://meu-app.com/login
  Quando preencho usuario "user@email.com" e senha "senha123"
  Entao devo ver a pagina inicial com mensagem "Bem-vindo"
```

O orquestrador vai:
1. Classificar os testes por tipo e executor
2. Coletar URL do ambiente, credenciais e configuracoes
3. Executar os testes em paralelo nos executores adequados
4. Gerar um relatorio HTML consolidado

### Gerar cenarios de teste a partir de uma historia de usuario

```
/qa-pipeline

Como usuario autenticado
Quero redefinir minha senha
Para recuperar acesso a minha conta
```

### Dry-run (visualizar o plano sem executar)

```
/orquestrador-qa --dry-run

[seus casos de teste aqui]
```

## Dependencias instaladas automaticamente em runtime

Os executores instalam pacotes Python e Node sob demanda durante a execucao:

| Executor | Instala automaticamente |
|---|---|
| executor-browser, executor-visual, executor-acessibilidade | `@playwright/test` + browsers Chromium/Firefox/WebKit |
| executor-api, executor-seguranca | `requests` (pip) |
| executor-banco | driver do banco (`psycopg2-binary`, `mysql-connector-python` ou `pyodbc`) |

## Documentacao completa

Consulte `CLAUDE.md` para a documentacao tecnica completa, incluindo arquitetura dos agentes, dependencias de runtime, historico de versoes e instrucoes de desenvolvimento.
