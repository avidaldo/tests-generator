# Customization Layer — Agent Instructions

## Purpose

This folder contains the VS Code and Copilot customization layer for repository maintenance. It is separate from the question-generation project surfaces in root `docs/` and root `prompts/`.

## Planning And Living Documentation

- `TODO:` is the default inline capture marker.
- `.github/implementation_plan.md` is the curated active plan. Question-style TODOs must be moved there as Clarification Queue entries before implementation starts.
- Use [`refresh-plan.prompt.md`](prompts/refresh-plan.prompt.md) to refresh the plan and surface unresolved questions before larger changes.
- Use [`implement-plan-item.prompt.md`](prompts/implement-plan-item.prompt.md) after the relevant plan item is approved.
- When a change affects customization architecture, workflow, or agent behavior, update the relevant `.github` docs and instruction files in the same change.
- Canonical rationale lives in [docs/customization_architecture.md](docs/customization_architecture.md).
- Hook rationale lives in [docs/agentic_enforcement_layers.md](docs/agentic_enforcement_layers.md).

## Customization Structure

| Path | Purpose |
| ---- | ------- |
| `prompts/` | Maintenance prompt launchers for the SDD loop |
| `agents/` | Custom agents for planning and implementation |
| `docs/` | Durable customization rationale and decision records |
| `instructions/` | File-scoped customization rules and sync adapters |
| `hooks/` | Deterministic guard rails and reminder hooks |
| `skills/` | Reusable auxiliary workflows with concrete second consumers |
| `README.md`, `AGENTS.md`, `implementation_plan.md` | Customization entry, inventory, and operational plan surfaces |

## Current VS Code Layout

- `.github/prompts/` is the default workspace prompt root in VS Code.
- Root `prompts/` stays enabled through `.vscode/settings.json` for the quiz-generation pipeline.
- `chat.useCustomAgentHooks` is enabled so planner-only guard rails can live with `todo-planner`.
- `chat.useNestedAgentsMdFiles` is enabled, so this file complements the root [../AGENTS.md](../AGENTS.md) rather than replacing it.

### Current Agents

- `todo-planner` — planning agent for the SDD loop; direct target of [`refresh-plan.prompt.md`](prompts/refresh-plan.prompt.md); owns clarification workflow and planner-only hooks.
- `sdd-implementer` — implementation agent for the SDD loop; direct target of [`implement-plan-item.prompt.md`](prompts/implement-plan-item.prompt.md); implements one approved item at a time and syncs docs.
- `batch-maintainer` — advanced optional maintenance agent for long unattended delegated or cloud-oriented runs; iterates through approved and unblocked items, keeps the plan and docs synced, and stops at unresolved decisions.

### Current Skills

- `customization-audit` — fetches current VS Code customization docs and audits this repo's `.github` customization files for deprecated patterns, missing recommended fields, and newly available primitives.
- `finish-question-coverage` — exhausts Stage 3 generation across an approved Stage 2 scope by tracking `SURF-*` coverage in a manifest and continuing with successive batches until the selected subcategories are done or blocked.
- `generate-question-batches` — runs the advanced Stage 3 bulk lane across multiple subcategory files, creating at most one new batch per subcategory while keeping checkpointed progress under a user-provided Stage 3 root.
- `summarize-all-sources` — fans out `summarize-sources.prompt.md` across multiple material paths and returns one summary per path.
- `notebook-hygiene` — installs the full four-layer notebook output enforcement stack.
- `editor-export` — exports reviewed editor JSON state to Moodle XML with explicit status control.

### Current Instructions

- `customization-authoring.instructions.md` — applies to `.github/instructions/*.instructions.md`, `.github/agents/*.agent.md`, and `.github/skills/**/SKILL.md`.
- `customization-documentation-sync.instructions.md` — applies to the `.github` customization docs, maintenance prompts, agents, instructions, and skills.
- `project-documentation-sync.instructions.md` — applies to the root project docs and question-generation prompts.
- `editor.instructions.md` — applies to `editor/**`.
- `markdown.instructions.md` — applies to `**/*.md`.
- `notebooks.instructions.md` — applies to `**/*.ipynb`.
- `prompt-authoring.instructions.md` — applies to `**/*.prompt.md` and `**/*.instructions.md`.
- `python.instructions.md` — applies to `**/*.py`.
- `resources.instructions.md` — applies to `resources/**`.
- `results.instructions.md` — applies to `results/**`.
- `xml-moodle.instructions.md` — applies to `**/*.xml`.

### Current Hooks

- `strip-notebook-outputs.json` — strips `.ipynb` outputs after agent file writes.
- `prompt-doc-drift-check.json` — reminds when prompt or customization edits lack matching doc updates.
- `living-docs-drift-check.json` — reminds when source edits have no matching plan or documentation updates.

## Update Rules

- Keep [copilot-instructions.md](copilot-instructions.md) as a thin VS Code adapter.
- When adding or removing customization files, update this file and the short customization summary in [../AGENTS.md](../AGENTS.md) in the same change.
- Keep maintenance prompt policy in [prompts/AGENTS.md](prompts/AGENTS.md).
- Keep project prompt policy in [../prompts/AGENTS.md](../prompts/AGENTS.md).
