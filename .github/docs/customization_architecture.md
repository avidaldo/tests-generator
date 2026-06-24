# Customization Architecture

## Purpose

This repository uses a small set of VS Code / Copilot customizations to support the
quiz-generation pipeline and keep documentation current. It is deliberately lean: there is
no spec-driven-development (SDD) maintenance loop.

> **Removed (kept here as a record).** An earlier version shipped an SDD loop:
> `.github/implementation_plan.md`, the `refresh-plan` / `implement-plan-item` /
> `run-batch-maintenance` prompts, the `todo-planner` / `sdd-implementer` /
> `batch-maintainer` agents, planner guard-rail hooks, and the living-docs / prompt-doc
> drift hooks. These were removed because the ceremony outweighed the benefit for a
> single-maintainer project. Plan larger changes against [../../todos.md](../../todos.md)
> using the built-in plan/agent tooling instead.

## Sources Of Truth

| Surface | Role |
| --- | --- |
| `TODO:` comments and [`todos.md`](../../todos.md) | Idea/bug/debt capture and the project backlog |
| `.github/docs/*.md` | Stable customization rationale and design decisions |
| `AGENTS.md`, `.github/AGENTS.md`, `*.instructions.md` | Agent behavior, routing, and always-on policy |

## Primitive Allocation

| Primitive | Role in this repo |
| --- | --- |
| Always-on instructions | Repo policy, routing, and behavior constraints present automatically in context |
| File instructions | File-type / module-specific rules applied via `applyTo` globs |
| Skills | Reusable orchestration helpers around the canonical quiz-generation prompts |
| Custom agents | Pipeline coordinators (`stage1-runner`, `stage3-runner`) and isolated workers (`batch-generator`, `source-summarizer`) |
| Hooks | Deterministic, judgment-free automation only |
| Prompts (root `prompts/`) | The canonical Stage 1–3 pipeline launchers |

## What Remains, And Why

- **Pipeline agents** (`stage1-runner`, `stage3-runner`, `batch-generator`, `source-summarizer`) — they do real fan-out/isolation work for summarization and exhaustive Stage 3 generation, and are Copilot CLI-compatible background lanes.
- **Skills** (`summarize-all-sources`, `generate-question-batches`, `finish-question-coverage`, `editor-export`, `customization-audit`, `notebook-hygiene`) — optional orchestration helpers around the canonical prompts; each packages reusable bulk/checkpoint/resume behavior that would clutter the prompt bodies.
- **One hook** (`strip-notebook-outputs.json`) — purely deterministic: strips `.ipynb` outputs after agent writes. This is the only behavior that justifies shell automation; everything judgment-heavy stays in the agent workflow.
- **Instructions and docs** — file-scoped coding rules and durable rationale.

## Hook Policy

Hooks are appropriate only for deterministic work (e.g. stripping notebook outputs). They must not author documentation or make editorial judgments; that belongs in the agent workflow. The repo currently keeps exactly one workspace hook for this reason.

## Docs Versus Instructions

- If the content explains *why* a design exists → `.github/docs/`.
- If it says *how* an agent should behave/route/prioritize → `AGENTS.md` or an instruction file.
- If it is a reusable multi-step workflow with a concrete second consumer → a skill.
- If it depends on a persona or isolation contract → a custom agent.
