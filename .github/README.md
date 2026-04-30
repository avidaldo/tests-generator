# Customization Layer

This folder contains the repository's VS Code and Copilot customization layer. It is intentionally separate from the question-generation project assets in root `docs/` and root `prompts/`.

## Preferred Entry Points

- Use [`refresh-plan.prompt.md`](prompts/refresh-plan.prompt.md) to refresh [.github/implementation_plan.md](implementation_plan.md).
- Use [`implement-plan-item.prompt.md`](prompts/implement-plan-item.prompt.md) to implement exactly one approved plan item.
- Use [`run-batch-maintenance.prompt.md`](prompts/run-batch-maintenance.prompt.md) only when you explicitly want the advanced unattended lane for approved and unblocked items; it stops on unresolved decisions instead of replacing the safe loop.
- `todo-planner`, `sdd-implementer`, and `batch-maintainer` remain visible as advanced or secondary entry points, but the prompts are the preferred UX.

## Canonical Files

- [AGENTS.md](AGENTS.md) — customization-layer policy and inventory.
- [docs/customization_architecture.md](docs/customization_architecture.md) — rationale for the prompt, agent, hook, and documentation split.
- [implementation_plan.md](implementation_plan.md) — active plan and decision log for maintenance work.
- [docs/agentic_enforcement_layers.md](docs/agentic_enforcement_layers.md) — case study and rationale for multi-layer enforcement.
- [docs/README.md](docs/README.md) — index for durable customization rationale and future decision records.
- [prompts/AGENTS.md](prompts/AGENTS.md) — maintenance prompt inventory.

## Layer Boundary

- Root `prompts/` is for the quiz-generation pipeline.
- Root `docs/` is for project and domain documentation.
- `.github/prompts/` is for repository-maintenance launchers.
- `.github/docs/` is for durable customization rationale and design records.
- `.github/README.md`, `.github/AGENTS.md`, and `.github/implementation_plan.md` are customization entry, inventory, and operational surfaces.
- `.github/agents/`, `.github/instructions/`, `.github/hooks/`, and `.github/skills/` are customization implementation surfaces.
