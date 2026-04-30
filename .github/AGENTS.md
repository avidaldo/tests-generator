# GitHub Automation — Agent Instructions

## Canonical Scope

This file is the canonical, tool-agnostic instruction surface for files under `.github/`.

- Keep `.github/copilot-instructions.md` as a lightweight VS Code adapter, not a second source of policy.
- Keep `.github/instructions/*.instructions.md` as routing adapters only.
- Keep `.github/implementation_plan.md` as the live queue and status file for the advanced unattended maintenance lane.
- Keep `.github/prompts/*.prompt.md` as the canonical prompt files for repository-maintenance workflows.

## Batch-Maintainer Workflow

- Refresh `.github/implementation_plan.md` before coding whenever `TODO:`, `ARCH:`, `DESIGN:`, `FIXME:`, or `HACK:` markers drift or the plan no longer matches repository state.
- Queue approved and unblocked work only. Move unresolved clarification or decision items to a blocked section instead of implementing them.
- Process one queue item at a time. After each completed item, update `.github/implementation_plan.md` and sync any directly affected docs or instruction files.
- In cloud or pull-request runs, stay on the current remote branch / PR isolation surface. Do not assume local-only branch workflows.
- Stop when the queue is empty or when the next item is blocked by unsafe repository state, unresolved decisions, or validation failures you cannot fix confidently within the current item.

## Maintenance Prompt Design

- Keep each maintenance prompt focused on one reusable workflow with explicit stop conditions.
- Prefer short checklists and output contracts over persona-heavy prose.
- When a maintenance prompt depends on repository state, make the required reads explicit in the prompt itself.
