# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Installation

Run the script below to install all agents into your local Claude Code profile. Restart Claude Code afterwards.

```powershell
.\install.ps1
```

## Purpose

This directory contains custom agent definitions for Claude Code. Each `.md` file defines a reusable agent (slash command) that can be invoked in any Claude Code session.

## Agent File Format

Each agent is a Markdown file with YAML frontmatter:

```markdown
---
name: agent-name
description: Short description shown in the agent picker
---

System prompt that defines the agent's behavior.
```

- `name`: becomes the slash command (e.g., `name: revisor` → `/revisor`)
- `description`: displayed when browsing available agents
- Body: the system prompt sent to Claude when the agent is invoked

## Existing Agents

- **revisor** — Revises texts in Brazilian Portuguese, correcting grammar, spelling, and clarity while preserving the author's tone.
- **gerador-criterios-aceite** — Generates acceptance criteria, a test plan, and a Mermaid mind map from a user story.
- **gerador-cenarios-teste** — Generates test scenarios from acceptance criteria in Gherkin, step-by-step, or CSV for Azure DevOps import.
- **qa-pipeline** — Orchestrator: receives a user story, generates acceptance criteria + test plan + mind map, then generates test scenarios in the user's chosen format (Gherkin, step-by-step, or Azure DevOps CSV).
