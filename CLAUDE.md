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

The QA agents follow an orchestrator → leaf pattern:

- **qa-pipeline** (orchestrator) — receives a user story, delegates to the two leaf agents in sequence, and manages the progressive format-offering loop
- **gerador-criterios-aceite** (leaf) — generates acceptance criteria, test plan, and Mermaid mind map from a user story
- **gerador-cenarios-teste** (leaf) — generates test scenarios (Gherkin, step-by-step, or Azure DevOps CSV) from acceptance criteria; handles progressive format delivery on its own when invoked standalone
- **revisor** (standalone) — text revision in Brazilian Portuguese, unrelated to the QA pipeline
- **consulta-treinamento** (standalone) — searches for a collaborator by name (fuzzy/partial match) in `~/Documents/3 - 28.04.26.xlsx` and displays their 2026 training progress with a visual percentage bar; requires the `openpyxl` Python package (installed automatically at runtime via `pip install openpyxl -q`)
- **classifier-testes** (standalone) — receives test cases in Gherkin, step-by-step, or Azure DevOps CSV format and returns structured JSON classifying each one by type (`smoke`, `sanity`, `regressão`, `e2e`, `integração`, `contrato`, `visual`, `acessibilidade`, `performance`, `carga`, `stress`, `soak`, `segurança`, `banco`, `cross-browser`, `mobile`, `data-driven`) and executor (`magnitude`, `http`, `k6`, `playwright-visual`, `axe-core`, `zap`, `db`, `pact`, `playwright-multibrowser`, `appium`, `parameterized`); excludes unit and manual tests automatically
- **orquestrador-qa** (orchestrator) — single entry point for the automation squad; receives test cases, invokes `classifier-testes`, dispatches to executor subagents in parallel, and presents the consolidated report from `reporter-qa`
- **executor-browser** (leaf) — runs browser/UI tests (smoke, sanity, regression, E2E, cross-browser) using Playwright
- **executor-api** (leaf) — runs API/integration tests via real HTTP requests with Python `requests`
- **executor-performance** (leaf) — runs performance, load, stress and soak tests using k6
- **executor-visual** (leaf) — runs visual regression tests using Playwright screenshot comparison
- **executor-acessibilidade** (leaf) — runs WCAG accessibility tests using axe-core via Playwright
- **executor-seguranca** (leaf) — runs non-invasive security checks (auth, headers, CORS, exposed endpoints) using Python
- **executor-banco** (leaf) — runs database integrity checks using Python; requires `DB_CONNECTION_STRING` env var; skips without asking if not set
- **reporter-qa** (leaf) — consolidates results from all executors into a structured report with summary, failures, and recommendations

Agents with `tools: ""` produce only text output: `gerador-criterios-aceite`, `gerador-cenarios-teste`, `classifier-testes`, and `reporter-qa`. The orchestrators (`qa-pipeline`, `orquestrador-qa`) and `consulta-treinamento` do not restrict tools.

## Adding a New Agent

1. Create `agents/<name>.md` with the frontmatter and system prompt.
2. Bump the `version` field in `.claude-plugin/plugin.json`.
3. Re-run `.\install.ps1` to deploy it.
4. Add it to the Agent Architecture section in this file.
