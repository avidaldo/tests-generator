# Customization Prompts — Agent Instructions

## Current State

This folder contains the canonical maintenance prompts for the repository. VS Code discovers this folder as the default workspace prompt root. The quiz-generation pipeline stays in [../../prompts/AGENTS.md](../../prompts/AGENTS.md).

| File | Status | Description |
| ---- | ------ | ----------- |
| `refresh-plan.prompt.md` | **Active — Planning Launcher** | Preferred slash-command entry for refreshing `.github/implementation_plan.md`; direct target of `todo-planner` |
| `implement-plan-item.prompt.md` | **Active — Implementation Launcher** | Preferred slash-command entry for implementing the next approved plan item; direct target of `sdd-implementer` |
| `run-batch-maintenance.prompt.md` | **Active — Advanced Batch Launcher** | Advanced optional slash-command entry for long unattended runs across approved and unblocked plan items; direct target of `batch-maintainer` |

## Design Notes

- These prompts are thin aliases. Durable workflow logic lives in the bound agents, not in prompt-body orchestration.
- Prompts are the preferred user-facing surface for maintenance work.
- `refresh-plan.prompt.md` and `implement-plan-item.prompt.md` remain the canonical precise workflow; `run-batch-maintenance.prompt.md` is the advanced unattended lane.
- `todo-planner`, `sdd-implementer`, and `batch-maintainer` remain visible as advanced or secondary entry points.
- Root `prompts/` is reserved for question-generation workflows.
