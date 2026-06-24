# Customization Layer

This folder contains the repository's VS Code and Copilot customization layer. It is intentionally separate from the question-generation project assets in root `docs/` and root `prompts/`.

> The earlier spec-driven-development (SDD) maintenance loop — `implementation_plan.md` plus the `refresh-plan` / `implement-plan-item` / `run-batch-maintenance` prompts and the `todo-planner` / `sdd-implementer` / `batch-maintainer` agents — was removed to keep this layer lean. Plan larger changes against [../todos.md](../todos.md) with the built-in plan/agent tooling instead.

## Preferred Entry Points

- Question generation runs from the root `prompts/` pipeline (`summarize-sources` → `merge-summaries` → `generate-questions`).
- Use [`skills/generate-question-batches/SKILL.md`](skills/generate-question-batches/SKILL.md) for the advanced Stage 3 bulk lane across multiple subcategory files (one batch per subcategory, checkpointed).
- Use [`skills/finish-question-coverage/SKILL.md`](skills/finish-question-coverage/SKILL.md) for the exhaustive Stage 3 lane that keeps batching until tracked `SURF-*` coverage is complete.
- The `stage1-runner` and `stage3-runner` agents are the background / Copilot CLI lanes for fan-out summarization and exhaustive generation.
- Use [`skills/customization-audit/SKILL.md`](skills/customization-audit/SKILL.md) when you need a periodic drift audit against the current VS Code customization docs.

## Canonical Files

- [AGENTS.md](AGENTS.md) — customization-layer policy and inventory.
- [docs/customization_architecture.md](docs/customization_architecture.md) — rationale for the agent, skill, hook, and documentation split.
- [docs/agentic_enforcement_layers.md](docs/agentic_enforcement_layers.md) — case study and rationale for multi-layer enforcement.
- [docs/README.md](docs/README.md) — index for durable customization rationale and future decision records.

## Layer Boundary

- Root `prompts/` is for the quiz-generation pipeline.
- Root `docs/` is for project and domain documentation.
- `.github/docs/` is for durable customization rationale and design records.
- `.github/README.md` and `.github/AGENTS.md` are customization entry and inventory surfaces.
- `.github/agents/`, `.github/instructions/`, `.github/hooks/`, and `.github/skills/` are customization implementation surfaces.
