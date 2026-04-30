# Customization Layer

This folder contains the repository's VS Code and Copilot customization layer. It is intentionally separate from the question-generation project assets in root `docs/` and root `prompts/`.

## Preferred Entry Points

- Use [`refresh-plan.prompt.md`](prompts/refresh-plan.prompt.md) to refresh [.github/implementation_plan.md](implementation_plan.md).
- Use [`implement-plan-item.prompt.md`](prompts/implement-plan-item.prompt.md) to implement exactly one approved plan item.
- `todo-planner` and `sdd-implementer` remain visible as advanced or secondary entry points, but the prompts are the preferred UX.

## Canonical Files

- [AGENTS.md](AGENTS.md) — customization-layer policy and inventory.
- [customization_architecture.md](customization_architecture.md) — rationale for the prompt, agent, hook, and documentation split.
- [implementation_plan.md](implementation_plan.md) — active plan and decision log for maintenance work.
- [agentic_enforcement_layers.md](agentic_enforcement_layers.md) — case study and rationale for multi-layer enforcement.
- [prompts/AGENTS.md](prompts/AGENTS.md) — maintenance prompt inventory.

## Layer Boundary

- Root `prompts/` is for the quiz-generation pipeline.
- Root `docs/` is for project and domain documentation.
- `.github/prompts/` is for repository-maintenance launchers.
- `.github/*.md`, `.github/agents/`, `.github/instructions/`, and `.github/hooks/` are the customization layer.
