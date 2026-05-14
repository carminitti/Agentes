# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Installation

Run the script below to install all agents into your local Claude Code profile. Restart Claude Code afterwards.

```powershell
.\install.ps1
```

The script first tries `claude plugin install --scope user` (preferred, requires plugin support). If unavailable, it falls back to copying the `.md` files from `agents/` directly to `~/.claude/agents/`.

If PowerShell blocks the script, run it with:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

## Purpose

This directory contains custom agent definitions for Claude Code. Each `.md` file in `agents/` defines a reusable agent (slash command) invokable in any Claude Code session.

## Plugin Structure

The plugin is registered via `.claude-plugin/plugin.json` (name: `qa-agents`, version: `1.1.0`). The `agents` field points to `./agents/`, which is the only directory the plugin distributes.

## Agent File Format

Each agent is a Markdown file with YAML frontmatter:

```markdown
---
name: agent-name
description: Short description shown in the agent picker
tools: ""          # optional — restrict available tools; omit to inherit all
---

System prompt that defines the agent's behavior.
```

- `name`: becomes the slash command (e.g., `name: revisor` → `/revisor`)
- `description`: displayed when browsing available agents
- `tools: ""`: explicitly disables all tools for the agent (used in leaf agents that only generate text)
- Body: the system prompt sent to Claude when the agent is invoked

## Agent Architecture

There are two independent orchestration pipelines plus standalone agents.

### Pipeline 1 — QA Planning (story → test scenarios)

`/qa-pipeline` → `gerador-criterios-aceite` → `gerador-cenarios-teste`

- **qa-pipeline** (orchestrator) — receives a user story, delegates to the two leaf agents in sequence, and manages the progressive format-offering loop
- **gerador-criterios-aceite** (leaf) — generates acceptance criteria, test plan, and Mermaid mind map from a user story
- **gerador-cenarios-teste** (leaf) — generates test scenarios (Gherkin, step-by-step, or Azure DevOps CSV) from acceptance criteria; handles progressive format delivery on its own when invoked standalone

### Pipeline 2 — Test Execution Squad (test cases → execution report)

`/orquestrador-qa` → `classifier-testes` → executor agents (parallel) → `reporter-qa`

- **orquestrador-qa** (orchestrator) — single entry point; receives test cases, invokes `classifier-testes`, dispatches to executor subagents in parallel, and presents the consolidated report
- **classifier-testes** (leaf) — classifies each test case by type (`smoke`, `sanity`, `regressão`, `e2e`, `integração`, `contrato`, `visual`, `acessibilidade`, `performance`, `carga`, `stress`, `soak`, `segurança`, `banco`, `cross-browser`, `mobile`, `data-driven`) and executor (`magnitude`, `http`, `k6`, `playwright-visual`, `axe-core`, `zap`, `db`, `pact`, `playwright-multibrowser`, `appium`, `parameterized`); excludes unit and manual tests
- **executor-browser** — runs browser/UI tests (smoke, sanity, regression, E2E, cross-browser) using Playwright; also handles `http` tests of types `smoke`/`sanity`/`regressão`/`e2e`
- **executor-api** — runs API/integration tests via real HTTP requests with Python `requests`; handles `http` tests of type `integração`
- **executor-performance** — runs performance, load, stress and soak tests using k6
- **executor-visual** — runs visual regression tests using Playwright screenshot comparison
- **executor-acessibilidade** — runs WCAG accessibility tests using axe-core via Playwright
- **executor-seguranca** — runs non-invasive security checks (auth, headers, CORS, exposed endpoints) using Python
- **executor-banco** — runs database integrity checks using Python; requires `DB_CONNECTION_STRING` env var; skips without asking if not set
- **executor-mobile** — runs native app tests (iOS/Android) using Appium with Python; requires a running Appium server and connected device/emulator; collects capabilities (platform, device, app package/bundle) in Etapa 2g before dispatching
- **reporter-qa** (leaf) — consolidates results from all executors into a structured report with summary, failures, and recommendations

> **`http` executor routing:** the `orquestrador-qa` routes `http`-classified tests to `executor-api` for `integração` type, and to `executor-browser` for `smoke`/`sanity`/`regressão`/`e2e` types.
> **`appium` routing:** the `orquestrador-qa` dispatches `appium`-classified tests to `executor-mobile`, passing capabilities collected in Etapa 2g (`appium_config`).

### Standalone Agents

- **revisor** — text revision in Brazilian Portuguese, unrelated to the QA pipeline
- **consulta-treinamento** — searches for a collaborator by name (fuzzy/partial match) in `~/Documents/3 - 28.04.26.xlsx` and displays their 2026 training progress with a visual percentage bar

### Tool restrictions

Agents with `tools: ""` produce only text output: `gerador-criterios-aceite`, `gerador-cenarios-teste`, `classifier-testes`, and `reporter-qa`. The orchestrators (`qa-pipeline`, `orquestrador-qa`) and `consulta-treinamento` do not restrict tools.

## Runtime Dependencies

The executor agents install lightweight Python/Node packages on demand, but some binaries must be present on the machine beforehand:

| Executor | Requires | Install hint |
|---|---|---|
| `executor-browser`, `executor-visual`, `executor-acessibilidade` | Node.js + `@playwright/test` + browser binaries | `npm install -D @playwright/test && npx playwright install chromium` |
| `executor-performance` | k6 binary | `winget install k6` (Windows) — **not installable via npm** |
| `executor-api`, `executor-seguranca` | Python + `requests` | `pip install requests` |
| `executor-banco` | Python + DB driver (`psycopg2-binary`, `mysql-connector-python`, or `pyodbc`) | installed automatically at runtime via `pip install -q` |
| `executor-mobile` | Python + `Appium-Python-Client` + Appium server running | `pip install Appium-Python-Client` — Appium server: `npm install -g appium && appium` |
| `consulta-treinamento` | Python + `openpyxl` | installed automatically at runtime via `pip install openpyxl -q` |

`executor-banco` also requires a `DB_CONNECTION_STRING` environment variable; without it, all bank tests are skipped automatically with no prompting.

## Example Test Inputs

The root contains sample test files that can be fed directly to `/orquestrador-qa`:

- `test_api.py` — 21 REST API test cases against `https://reqres.in/api` (GET, POST, PUT, PATCH, DELETE, auth)
- `test_perf.py` — 1 performance test case (delayed endpoint, validates response > 3 s)
- `test_security.py` — 1 security test case (verifies 401 on missing API key)

These are not runnable Python unit tests — they are natural-language test case definitions consumed by the squad agents.

## Runtime Artifacts

The executor agents generate ephemeral files in the repository root during test runs: `tmp_*.py`, `tmp_*.js`, and `tmp_*.json`. These are covered by `.gitignore` and should not be committed.

## Integração com claude.ai

O arquivo `claude_ai_project_instructions.md` contém o system prompt consolidado que replica o squad completo no claude.ai — classificação, execução e relatório em conversa única, sem subagentes.

### Setup

1. **Inicie o MCP server** com transporte HTTP (necessário para claude.ai web):
   ```powershell
   pip install -r mcp_server/requirements.txt
   python mcp_server/server.py --transport sse --port 8000
   ```
   Para uso local sem exposição pública, use um tunnel:
   ```powershell
   # ngrok
   ngrok http 8000
   # ou cloudflared
   cloudflare tunnel --url http://localhost:8000
   ```

2. **Registre o MCP no claude.ai:** `Settings → Integrations → Add integration` — informe a URL pública gerada pelo tunnel (`https://<id>.ngrok.io`).

3. **Crie um Project no claude.ai** e cole o conteúdo de `claude_ai_project_instructions.md` em **Project Instructions**.

4. **Use:** envie os casos de teste diretamente na conversa do Project. O squad classifica, executa via MCP tools e entrega o relatório.

> Para uso com **Claude Desktop** (local, sem tunnel): configure stdio no `claude_desktop_config.json` apontando para `python mcp_server/server.py`. Nesse caso, omita `--transport sse`.

### Diferença vs Claude Code

| | Claude Code (`/orquestrador-qa`) | claude.ai (Project) |
|---|---|---|
| Execução | Paralela (subagentes) | Sequencial (uma tool por vez) |
| Contexto | Isolado por agente | Único, cresce com resultados |
| Setup | Só instalar o plugin | MCP server + tunnel/deploy |

---

## MCP Server

`mcp_server/server.py` is an optional FastMCP server (`qa-squad`) that exposes low-level execution tools so the executor agents can run scripts without needing native tool access:

| Tool | What it does |
|---|---|
| `execute_python(code)` | Writes code to a temp file and runs it with the current Python interpreter |
| `execute_node(script)` | Runs a Node.js script (Playwright, axe-core) |
| `execute_k6(script)` | Runs a k6 performance script |
| `run_api_tests(base_url, tests_json)` | High-level structured REST test runner |
| `run_security_checks(base_url, extra_endpoints)` | Non-invasive security header / CORS / sensitive-endpoint checker |
| `run_performance_test(url, vus, duration, threshold_p95_ms)` | One-call k6 load test |

Install dependencies and start the server:

```powershell
pip install -r mcp_server/requirements.txt
python mcp_server/server.py
```

`requirements.txt` pins `mcp[cli]>=1.0.0` and `requests>=2.31.0`. The executor agents work without the MCP server (they call Python/Node/k6 directly via the `Bash` tool), but the server is useful when tool access is restricted.

## Adding a New Agent

1. Create `agents/<name>.md` with the frontmatter and system prompt.
2. Bump the `version` field in `.claude-plugin/plugin.json`.
3. Re-run `.\install.ps1` to deploy it.
4. Add it to the Agent Architecture section in this file.

## Version History

| Version | Changes |
|---|---|
| v1.1.0 | Squad base criado |
| v1.2–1.7 | Logs, POM, auth, SSL, classifier, etc. |
| v1.8.0 | Acessibilidade e segurança corrigidos |
| v1.9.0 | Logs nos 5 executores restantes |
| v1.10.0 | Orquestrador — coleta centralizada de auth/URL |
| v1.11.0 | 7 executores com Prioridade 0 (contexto orquestrador) |
| v1.12.0 | 5 correções de auditoria |
| v1.13.0 | 7 correções críticas |
| v1.14.0 | Correções A, B, C |
| v1.15.0 | Correções D, E, F, G, H |
| v1.15.1 | Auto-registro browser + cobertura total reporter |
| v1.15.2 | Executor-banco modo real/simulado |
| v1.15.3 | Otimizações de velocidade e tokens |
| v1.15.4 | Correções de confiabilidade e integridade |
| v1.16.0 | Classificação de ambiente, `known_demo_failure`, install automático banco |
| v1.16.1 | Reporter-qa: separação bloqueantes vs não-bloqueantes |
| v1.17.0 | 13 correções críticas (`networkidle`, `DEMO_HOSTS`, `beforeAll`, CORS OPTIONS, etc.) |
| v1.18.0 | 6 bugs críticos: `domcontentloaded` no visual, `SETUP_FAILED` em specs browser/api, parallel exceptions no segurança, `mysql.connector` com urlparse, `low_confidence` visível no orquestrador e reporter |
| v1.19.0 | Suite directory (`suite_[nome]_[timestamp]/`), `execution.log` em todos os executores, `credentials_failed` signal + retry loop no orquestrador, `suite_dir` propagado no contexto |
| v1.19.1 | 8 bugs críticos/graves: `credentials_failed` via arquivo (não process.env), `suiteDir` declarado no TS, suite_dir via Bash (não pseudocódigo), banco conflito null resolvido, `connect_timeout` com ThreadPoolExecutor, soak 10min→3min, auth timeout 5s por endpoint, cache npm via junction/symlink, `workers` CI-aware |
| v1.23.0 | Lean mode redesenhado: arquivo único por executor, sem screenshots/vídeos/logs em disco, execução sequencial, resumo inline no chat (sem reporter-qa, sem relatório em disco), isenção de perguntas 2f desnecessárias |
| v1.24.0 | Modo técnico do reporter detalhado: classificação de tipo de erro, resposta raw completa, aba Código mostra apenas o bloco do TC com linha falhou marcada, diff esperado×obtido específico por executor, stack trace opcional |
| v1.25.0 | 6 correções: lean browser usa JS puro (node) em vez de ts-node; executor-api cache Windows com fallback; seção lean_mode morta removida do classifier; profile save corrige report_output_dir em lean mode; aviso cross-browser em lean mode; descrição "Sem relatório HTML em disco" |
| v1.25.1 | executor-mobile documentado no CLAUDE.md (Pipeline 2, Runtime Dependencies) |
| v1.25.2 | 2 bugs críticos: lean visual usa JS+config (não ts-node) com snapshotDir correto; `--rerun-failed` bloqueia em lean mode com aviso explícito |
| v1.25.3 | 3 bugs críticos: executor-banco `_re.compile` (NameError com `import re as _re`); lean visual `workers:1` ausente no config; orquestrador "único arquivo" contradição com visual (2 arquivos) |
| v1.25.4 | 5 gaps de qualidade: parameterized routing ambíguo no orquestrador; mobile sem `generated_files` no output; mobile sem instrução `SUITE_DIR` para execução; segurança sem `skipped:0` no summary; reporter lean mode (código morto — orquestrador nunca invoca reporter em lean mode) |
